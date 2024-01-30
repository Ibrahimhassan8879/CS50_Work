document.addEventListener('DOMContentLoaded' , function() {
    let correct_button = document.querySelector('#correct')
let Incorrect_button = document.querySelector('#Incorrect')

if (correct_button.addEventListener('click'))
{
    correct_button.style.background ='green';
    console.log("hi");

}
else
{
Incorrect_button.addEventListener('click' , function(){
    Incorrect_button.style.background = 'red';
    console.log("hello");
});
};

});




