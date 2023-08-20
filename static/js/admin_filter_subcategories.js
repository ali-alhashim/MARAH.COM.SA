// admin_filter_subcategories.js

(function($) {
    $(document).ready(function() {
        var categoryField = $('#id_category');

        categoryField.change(function() {
            var categoryId = $(this).val();
            var subCategoryField = $('#id_sub_category');

            // Clear existing options
            subCategoryField.find('option').remove();

            // Fetch subcategories via AJAX
            $.ajax({
                url: '{% url "get_subcategories" %}',  // Replace with your URL to fetch subcategories
                data: {'category_id': categoryId},
                success: function(data) {
                    $.each(data, function(key, value) {
                        subCategoryField.append($('<option></option>').attr('value', key).text(value));
                    });
                }
            });
        });
    });
})(jQuery);