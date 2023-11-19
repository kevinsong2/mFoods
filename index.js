// Spoonacular API key but this should be somehow hidden. Need to fix this for security purposes
const apiKey = 'c07aa86ecf084405b55efbf79ac910a5';
console.log("connected")
$(function() {
  document.getElementById('imageInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (!file.type.match('image.*')) {
        alert('Please select an image file.');
        return;
    }

    var formData = new FormData();
    formData.append('file', file); // Append the file to FormData

    fetch('http://localhost:5000/model/views/upload', { // Make sure this URL matches your Flask route
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Call a function to display the ingredients
        displayIngredients(data.ingredients);
    })
    .catch(error => console.error('Error during fetch:', error));
});

    function displayPredictedIngredients(prediction, ingredients) {
      var ingredientsList = `<h3>Predicted Recipe: ${prediction}</h3><ul>`;
      ingredients.forEach(function(ingredient) {
          ingredientsList += `<li>${ingredient}</li>`;
      });
      ingredientsList += '</ul>';
      
      $('#recipeOp').html(ingredientsList);
    }
    
    $('form').on("submit", function(e){
        e.preventDefault();
        loading();
        
        // Recongizes commas and trims spaces to put them into seperate lists
        const userInput = $('#search-bar').val();
        const ingredientsArray = userInput.split(',');
        ingredientsArray.forEach(ingredient => {
          const listItem = `<li>${ingredient.trim()}</li>`; // trim to remove extra spaces
          $('#ingredient-list').append(listItem);
      });
        
        async function getFood() {
          const response = await fetch(
            `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${
              $('#search-bar').val()
            }&number=5&apiKey=${apiKey}`
          );
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const items = await response.json(); // the JSON body content.
          console.log(items);
          removeLoading();
        //   displayFirstRecipe(items); // Remove this later
          foodID(items);
        }
    
        function foodID(items) {
          items.forEach((item, i) => {
              fetch(`https://api.spoonacular.com/recipes/${item.id}/information?apiKey=${apiKey}`)
                .then(data => data.json()).then(recipe => getRecipe(recipe, item.image));
                
            });
        }
        
        //// !!!<TEMP FUNCTION TO TEST>!!! ///
        // function displayFirstRecipe(items) {
        //     if (items.length > 0) {
        //         const firstItem = items[0];
        //         fetch(`https://api.spoonacular.com/recipes/${firstItem.id}/information?apiKey=${apiKey}`)
        //             .then(data => data.json())
        //             .then(recipe => getRecipe(recipe, firstItem.image));
        //     }
        // }

        function getRecipe(item, image) { 
          // Create HTML content for each title
          const title = `<h5 class="card-title recipe-title" data-id="${item.id}">${item.title}</h5>`;
          $('#recipeTitle-list').append(title);  //appending to list made in html
          $(title).on("click", function() {
            window.open(
            `https://api.spoonacular.com/recipes/${item.id}/information?apiKey=${apiKey}`,
            '_blank' 
            );
        });
        
        // $('#recipeTitle-list').append(title); // THIS HERE is causing double
          let details = item.extendedIngredients;
    
          let getAmount = details.map(ingAmt => {
              return ingAmt.original;
            });
              
        
    
          const recipe = `
            <div class="card" style="width: 18rem;">
              <h5 class="card-title" id="recipeName">${item.title}</h5>
              <img class="card-img-top"id="image" src="${image}" alt="Card image cap" />
              <button id="${item.id}" type="button"  class="btn btn-warning">PICK THIS RECIPE</button>
              <div class="card-body">
                <p class="card-text" id="recipe">${item.summary}</p>
              </div>
            </div>`;
          $('#recipeOp').append(recipe);
    
        $(`#${item.id}`).on("click", function() {
          
          $('#recipeOp').empty();
              
          $(function () {
            $("#tabs").tabs();
          });
    
            const recipeChoice =`
                <div id= "tabs">
                    <ul>
                     <li><a href="#tabs-1">Meal</a></li>
                     <li><a href="#tabs-2">Ingredients</a></li>
                     <li><a href="#tabs-3">Directions</a></li>
                   </ul>
                   <div id="tabs-1">
                     <h3>${item.title}</h3>
                     <img src="${image}" alt="Meal Image">
                     
                   </div>
                   <div id ="tabs-2">   
                    <h5>Ingredients:</h5>
                    <ul>
                    ${getAmount
                      .map((ingredient) => `<li>${ingredient}</li>`)
                      .join("")}
    
                    </ul>
                   </div>
                   <div id="tabs-3">
                    <h4>${item.title}</h4>
                    <p>${item.instructions}</p>
                    </div>`;
                  $('#recipeOp').append(recipeChoice);
          });
        }
        $('#recipeOp').empty();
        getFood();
      });
});


function loading (){
    $(".container").append("<div class = 'loading'><img src= 'static/images/loading.gif'></div>")
} 
  
function removeLoading (){
    $(".loading").remove();
}


// console.log("connected")
// $(function() {
//     $('form').on("submit", function(e) {
//         e.preventDefault();
//         loading();

//         // Recognizes commas and trims spaces to put them into separate lists
//         const userInput = $('#search-bar').val();
//         const ingredientsArray = userInput.split(',');
//         ingredientsArray.forEach(ingredient => {
//             const listItem = `<li>${ingredient.trim()}</li>`; // trim to remove extra spaces
//             $('#ingredient-list').append(listItem);
//         });

//         const title = `<h5 class="card-title recipe-title" data-id="hello">TESTING WORLD</h5>`;
//         $('#recipeTitle-list').append(title);  //appending to list made in html
//         // Simulate recipe display without calling the API
//         displayRecipe();

//         removeLoading();
//     });
// });

// function displayRecipe() {
//     const recipeTitle = "Testing for Recipes";
//     const image = "path_to_default_image.jpg"; // Replace with a default image path
//     const recipeSummary = "This is a test summary for the recipe.";

//     const recipe = `
//         <div class="card" style="width: 18rem;">
//             <h5 class="card-title" id="recipeName">${recipeTitle}</h5>
//             <img class="card-img-top" id="image" src="${image}" alt="Card image cap" />
//             <div class="card-body">
//                 <p class="card-text" id="recipe">${recipeSummary}</p>
//             </div>
//         </div>`;
//     $('#recipeOp').append(recipe);
// }

// function loading() {
//     $(".container").append("<div class = 'loading'><img src= 'static/images/loading.gif'></div>")
// }

// function removeLoading() {
//     $(".loading").remove();
// }
