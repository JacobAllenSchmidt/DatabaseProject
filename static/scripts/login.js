const emailFormCustomer = document.getElementById("email_form_customer");
const emailFormContractor = document.getElementById("email_form_contractor");

emailFormCustomer.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = new FormData(emailFormCustomer);
    
    const response = await fetch('/login', {
        method: 'POST',
        body: data
    });
    const result = await response.json();
    console.log(response);
    console.log(result);

    if (result.status == "error") {
        alert(result.message);
    }

});

emailFormContractor.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = new FormData(emailFormContractor);
    
    const response = await fetch('/login', {
        method: 'POST',
        body: data
    });
    const result = await response.json();
    console.log(response);
    console.log(result);
});