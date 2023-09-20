var isLoading = false;
var page = 2; // Initial page number (if applicable)

function loadMoreData() {
    if (isLoading) return;
    isLoading = true;
    $.ajax({
        url: '/load_more_data/',  // URL to your Django view
        data: {'page': page},      // Additional data to pass to the view
        dataType: 'json',
        success: function(data) {
            if (data.has_more) {
                $('#data-container').append(data.html);
                page++;
            }
            isLoading = false;
        }
    });
}

$(document).ready(function() {
    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $('#data-container').height() - 200) {
            loadMoreData();
        }
    });
});