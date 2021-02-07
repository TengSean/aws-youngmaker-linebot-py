/*	gallery */
$(document).ready(function(){

    $(".filter-button").click(function(){
        var value = $(this).attr('data-filter');
        document.getElementById("data-filter-now").setAttribute("data-filter-now",value);
        
        if(value == "all")
        {
            $('.filter').show('1000');
        }
        else
        {
            $(".filter").not('.'+value).hide('3000');
            $('.filter').filter('.'+value).show('3000');
            
        }

        if ($(".filter-button").removeClass("active")) {
            $(this).removeClass("active");
        }
        $(this).addClass("active");
    });
});


function loadItems() {
    var scroller = document.querySelector("#scroller");
    var template = document.querySelector('#post_template');
    var sentinel = document.querySelector('#sentinel');
    var filter_now = document.getElementById("data-filter-now").getAttribute("data-filter-now");
//     alert(filter_now);
    var counter = 0;

  // Use fetch to request data and pass the counter value in the QS
  fetch(`/load?c=${counter}`).then((response) => {

    // Convert the response data to JSON
    response.json().then((data) => {

      // If empty JSON, exit the function
      if (!data.length) {

        // Replace the spinner with "No more posts"
        sentinel.innerHTML = "No more posts";
        return;
      }

      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {

        // Clone the HTML template
        let template_clone = template.content.cloneNode(true);
        if (filter_now === "category1"){

        // Query & update the template content
            template_clone.querySelector("#iimg").src="https://picsum.photos/400/250?image=486";
            template_clone.querySelector("#aimg").setAttribute("data-fancybo","category1");
            template_clone.querySelector("#dimg").className+=" category1";

//                 template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
//                 template_clone.querySelector("#content").innerHTML = data[i][2];
        }else if (filter_now === "category2"){
            template_clone.querySelector("#iimg").src="https://picsum.photos/400/250?image=846";
            template_clone.querySelector("#aimg").setAttribute("data-fancybo","category2");
            template_clone.querySelector("#dimg").className+=" category2";
        }
        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;

        // Update the counter in the navbar
      }
    })
  })
}
/*	end gallery */
// $(document).ready(function(){
window.onload = function() {
    // Get references to the dom elements

    var sentinel = document.querySelector('#sentinel');
    var filter = "All";

    var intersectionObserver = new IntersectionObserver(entries => {
      // If intersectionRatio is 0, the sentinel is out of view
      // and we don't need to do anything. Exit the function
      if (entries[0].intersectionRatio <= 0) {
        return;
      }
      loadItems();
    });
    intersectionObserver.observe(sentinel);    
};

$(document).ready(function(){
    $(".fancybox").fancybox({
        openEffect: "none",
        closeEffect: "none",
    });
});
   
  