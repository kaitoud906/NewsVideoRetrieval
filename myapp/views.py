from django.shortcuts import render

from videoretrieval.settings import MEDIA_URL, USE_VIDEO

from myapp.models import DataStorage, CLIPEmbedding

from myapp.forms import FilterForm

import numpy as np

import os

def index(request):
    return render(request, 'myapp/index.html')

def get_score_for_each_query(kf_lst, query_results,video):
    tmp_score = 0
    for query_idx in query_results[video]:
        for kf in query_results[video][query_idx]:
            if kf in kf_lst:
                tmp_score+=4
                break
    return tmp_score

def group_items_by_threshold(query_results,lst, video, threshold=2):
    lst.sort()
    grouped_items = []
    current_group = [lst[0]]

    for i in range(1, len(lst)):
        if abs(int(lst[i]) - int(lst[i-1])) <= threshold:
            current_group.append(lst[i])
        else:
            score = get_score_for_each_query(current_group,query_results,video)
            
            grouped_items.append([video,current_group,[0,score,0,0]])
            current_group = [lst[i]]
    

    score = get_score_for_each_query(current_group,query_results,video)
            
    grouped_items.append([video,current_group,[0,score,0,0]])  # Append the last group

    return grouped_items

def max_child_length(item):
    # return total score
    return item[2][0] + item[2][1] + item[2][2] + item[2][3]

def display_images(request):
    # Get a list of image filenames in the 'media' directory
    k = 100
    query_text = ['']
    weight = [1]
    pre_similar = True
    case = 'single'
    threshold = 2
    if request.method == 'POST':
        # Get the query text entered by the user
        query_text = request.POST.getlist('query[]')
        k = int(request.POST.get('k'))
        form = FilterForm(request.POST or None)
        weight =  request.POST.getlist('weight[]')
        threshold = request.POST.get('threshold')
        
        if form.is_valid():
            case = form.cleaned_data.get('filter_by')
        
        
        top_k_images = DataStorage.all_path[:k]
        # if query_text == '':
        #     top_k_images = DataStorage.all_path[:k]
        # else:
        if case == 'single':
            query = query_text[0]
            if query == '':
                top_k_images = DataStorage.all_path[:k]
            else:
                query_embedding = get_single_text_embedding(query).astype('float32')

                distances, indices = DataStorage.index.search(query_embedding, k)

                top_k_images = DataStorage.all_path[indices].squeeze(0).tolist()

        elif case == 'multiple':
            top_k_images = get_multiple_result(query_text,weight,k,threshold)
                
    else:
        top_k_images = DataStorage.all_path[:k]
        # print(top_k_images[0]) # keyframes\L01_V001\0001.jpg
        
    image_urls = []
    for e in top_k_images:
        node = {
          "url": MEDIA_URL + e.replace('\\', '/'),
          "frame_id": e.split("\\")[-1].split(".")[0],
          "video": e.split("\\")[1]
        }
        image_urls.append(node)
    response = {
        'image_urls': image_urls, 
        'old_data': zip(query_text,weight), 
        "old_k": k,
        'old_threshold':threshold,
        "selected_option": case
    }

    return render(request, 'myapp/index.html', response)

def get_single_text_embedding(text):
    inputs = CLIPEmbedding.tokenizer(text, return_tensors = "pt")
    text_embeddings = CLIPEmbedding.model.get_text_features(**inputs)
    # convert the embeddings to numpy array
    embedding_as_np = text_embeddings.cpu().detach().numpy()
    return embedding_as_np

def get_multiple_result(query_text,weight,k,threshold):
    query_results = {}

    print(weight)

    for query_idx, query in enumerate(query_text):
        query_embedding = get_single_text_embedding(query).astype('float32')

        distances, indices = DataStorage.index.search(query_embedding, k)

        top_k_images = DataStorage.all_path[indices].squeeze(0).tolist()

        for result_idx,item in enumerate(top_k_images):
            kf_id = item.split("\\")[-1].split(".")[0]
            video = item.rsplit("\\",1)[0]
            if video not in query_results:
                # if video has not existed, create video key and first result query
                query_results[video] = {}
                query_results[video][str(query_idx)] = [kf_id]
                # create score field
                query_results[video]['score'] = {}
            else:
                # save result frames query according to query order
                if str(query_idx) not in query_results[video]:
                    query_results[video][str(query_idx)] = [kf_id]
                else:
                    query_results[video][str(query_idx)].append(kf_id)

            # save frame score based on result of query
            # if int(video[1:3])>=10:
            #     score = round((k-result_idx)/(100),1)*4
            #     # video from L10 has lower score (lower confidence) because it has lower quality
            # else:
            score = round((k-result_idx)/(100),1)*4* float(weight[query_idx])
            if result_idx not in query_results[video]['score']:
                query_results[video]['score'][kf_id] = score
            else:
                query_results[video]['score'][kf_id] += score

    result = []
    for video,frame_lst in query_results.items():
        merge_frame_lst = []
        for query_order in frame_lst:
            if query_order == 'score': continue
            merge_frame_lst+=frame_lst[query_order]

        result += [[video,merge_frame_lst]]

    last_result = []
    for i in range(len(result)):
        video, frame_lst = result[i][0],result[i][1]
        last_result+= group_items_by_threshold(query_results,frame_lst,video,threshold=int(threshold))
    
    for item in last_result:
        unique_frame = np.unique(item[1]) # return np array unique of frame list
        video = item[0]
        score = item[2]
        for frame in unique_frame:
            score[0]+= query_results[video]['score'][str(frame)]
        score[0]/=unique_frame.shape[0]
        # print()
        duplicate_count = sum(np.array([item[1].count(x) for x in unique_frame])>1)
        if duplicate_count == 0:
            score[2] +=3
        elif duplicate_count <= 2:
            score[2]+=1
        
        # bonus score for many frame
        # bonus_score = min(unique_frame.shape[0],len(query_split))*0.3
        # bonus_score = min(len(item[1]),len(query_split))*0.2
        bonus_score = unique_frame.shape[0]*0.2
        score[3] += bonus_score
        item.append(unique_frame)
    
    last_result = sorted(last_result, key=max_child_length, reverse=True)
    top_k_images = []
    for item in last_result:
        top_k_images.append(os.path.join(item[0],item[3][0]+".jpg"))
    return top_k_images