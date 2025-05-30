document.addEventListener("DOMContentLoaded", function () {
    //creaate a varable for the buttons
    let btn = document.querySelector('#btn')
    let sidebar = document.querySelector('.sidebar')

btn.addEventListener("click",btnButton)

function btnButton(){
     sidebar.classList.toggle('active')
}


//view customer details
   const customerButtons = document.querySelectorAll(".customer-name");

  function loadCustomerDetails(id) {
    fetch(`/api/customers/${id}/`)
      .then(response => response.json())
      .then(data => {
      
        document.getElementById("names").textContent = data.name;
        document.getElementById("emails").textContent = data.email;
        document.getElementById("phones").textContent = data.phone_no;
        document.getElementById("estates").textContent = data.estate;
        document.getElementById("plots").textContent = data.plot_no;

        document.getElementById("edit-btn").href = `/customers/edit/${data.id}/`;
        document.getElementById("delete-btn").href = `/customers/delete/${data.id}/`;
        document.getElementById("action-buttons").style.display = "block";
      })
      .catch(error => {
        console.error("Error fetching customer data:", error);
      });
  }

  // Load first customer by default
  const firstButton = document.querySelector('.customer-name[data-default="true"]');
  if (firstButton) {
    loadCustomerDetails(firstButton.getAttribute("data-id"));
  }

  // Handle clicks
  customerButtons.forEach(button => {
    button.addEventListener("click", function () {
      const id = this.getAttribute("data-id");
      loadCustomerDetails(id);
    });
  });

  //
   const params = new URLSearchParams(window.location.search);
    const highlightId = params.get("highlight");
    if (highlightId) {
      const el = document.getElementById("highlight-" + highlightId);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        el.style.background = "#ffffcc";  // Optional highlight
           setTimeout(() => {
        el.style.backgroundColor = "";  // Remove highlight after a moment
      }, 3000);
      }
    }

  //service history form navigation
  const serviceTypeSelect = document.getElementById('serviceTypeSelect');
const normalFields = document.getElementById('normalFields');
const specialFields = document.getElementById('specialFields');


if (serviceTypeSelect && normalFields && specialFields){
function updateFormFields() {
  const selected = serviceTypeSelect.value;

  // Reset visibility
  normalFields.style.display = 'block';
  specialFields.style.display = 'none';


  if (selected === 'normal') {
    normalFields.style.display = 'block';
  } else if (selected === 'special') {
    specialFields.style.display = 'block';
    normalFields.style.display = 'none';

  } 
}


serviceTypeSelect.addEventListener('change', updateFormFields);

// Run on load
updateFormFields();
}


//showing all the services available for invoice generator
//view customer details
const select = document.getElementById("service");

if (select) {
  select.addEventListener("change", function () {
    const selectedOption = select.options[select.selectedIndex];
    const name = selectedOption.value;
    const type = selectedOption.getAttribute("data-type");

    console.log("Selected:", { name, type });

    fetch(`/api/service-by-name/?name=${encodeURIComponent(name)}`)
      .then(response => response.json())
      .then(data => {
        const serviceList = document.getElementById("service-list");
        serviceList.innerHTML = ""; // Clear previous options

        if (data.length === 0) {
          const emptyOption = document.createElement("option");
          emptyOption.disabled = true;
          emptyOption.textContent = "No services found";
          serviceList.appendChild(emptyOption);
        } else {
          data.forEach(service => {
            const option = document.createElement("option");
            option.value = service.id; // assuming `id` is returned in API
            option.textContent = `${service.service_description} - R${service.price}`;
            serviceList.appendChild(option);
          });
        }

        document.querySelector(".services_available").style.display = "block";
      })
      .catch(error => {
        console.error("Error fetching services:", error);
      });
  });
}

//makethe select all in service invoices to select allservices
const selectAllCheckbox = document.getElementById("select-all-services");

selectAllCheckbox.addEventListener("change", () => {
  const options = document.getElementById("service-list").options;
  for (let option of options) {
    option.selected = selectAllCheckbox.checked;
  }
});

  
// Pre-fill today's date for the date input in service history form
const today = new Date().toISOString().split('T')[0];
const dateInput = document.getElementById('serviceDateInput')
if (dateInput) {
  dateInput.value = today;
}

})
