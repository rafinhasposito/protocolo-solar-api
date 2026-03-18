const mainContainer = document.getElementById("main-container");
const formContainer = document.getElementById("form-container");
const topImage = document.getElementById("top-image");
const topTitle = document.getElementById("top-title");
const heading = document.getElementById("heading");
const paragraph = document.getElementById("paragraph");
const formAction = document.getElementById("form-action");
const resultContainer = document.getElementById("result-container");
const resultHeading = document.getElementById("result-heading");
const resultSign = document.getElementById("result-sign");
const errorContainer = document.getElementById("error-container");
const errorMessage = document.getElementById("error-message");
const calBtn = document.getElementById("cal-btn");
const resultSun = document.getElementById("result-sun");
const resultMoon = document.getElementById("result-moon");
const resultMercury = document.getElementById("result-mercury");
const resultVenus = document.getElementById("result-venus");
const resultMars = document.getElementById("result-mars");
const resultJupiter = document.getElementById("result-jupiter");
const resultSaturn = document.getElementById("result-saturn");
const resultUranus = document.getElementById("result-uranus");
const resultNeptune = document.getElementById("result-neptune");
const resultPluto = document.getElementById("result-pluto");
const resultAsc = document.getElementById("result-asc");


let formType = "";

const API_URL = "https://api.birthchartstore.com";

[formContainer, resultContainer, errorContainer].forEach(el => el.style.display = "none");


let allCities = [];

const fetchCountriesAndCities = () => {
  var headers = new Headers();
  headers.append("X-CSCAPI-KEY", "MWRDbWJtMnFqZW5SbXNZUno1b0tMUDQ1MlprTzFGdVc0dERPVjlTTQ==");

  var requestOptions = {
    method: 'GET',
    headers: headers,
    redirect: 'follow'
  };

  fetch("https://api.countrystatecity.in/v1/countries", requestOptions)
    .then(response => response.json())
    .then(countries => {
      const citySelect = document.getElementById('city');
      
      // Use Promise.all to fetch cities for all countries concurrently
      Promise.all(countries.map(country => 
        fetch(`https://api.countrystatecity.in/v1/countries/${country.iso2}/cities`, requestOptions)
          .then(response => response.json())
          .then(cities => ({country, cities}))
      ))
      .then(results => {
        results.forEach(({country, cities}) => {
          cities.forEach(city => {
            const cityOption = `${city.name}, ${country.name}`;
            allCities.push(cityOption);
            const option = document.createElement('option');
            option.value = cityOption;
            option.textContent = cityOption;
            citySelect.appendChild(option);
          });
        });

        convertSelectToDatalist();
      })
      .catch(error => console.error('Error fetching cities:', error));
    })
    .catch(error => console.error('Error fetching countries:', error));
};

const convertSelectToDatalist = () => {
  const citySelect = document.getElementById('city');
  const cityInput = document.createElement('input');
  cityInput.type = 'text';
  cityInput.id = 'city';
  cityInput.name = 'city';
  cityInput.setAttribute('list', 'cityList');
  cityInput.placeholder = 'Type to search for a city';
  cityInput.className = citySelect.className;

  const datalist = document.createElement('datalist');
  datalist.id = 'cityList';

  citySelect.parentNode.replaceChild(cityInput, citySelect);
  cityInput.parentNode.appendChild(datalist);

  cityInput.addEventListener('input', filterCities);
};

const filterCities = (e) => {
  const filterValue = e.target.value.toLowerCase();
  const datalist = document.getElementById('cityList');
  
  datalist.innerHTML = '';

  const filteredCities = allCities.filter(city => 
    city.toLowerCase().includes(filterValue)
  );

  filteredCities.forEach(city => {
    const option = document.createElement('option');
    option.value = city;
    datalist.appendChild(option);
  });
};

fetchCountriesAndCities();

const showForm = (title, imageSrc, type) => {
  formContainer.style.display = "block";
  mainContainer.style.display = "none";

  topImage.src = imageSrc;
  topTitle.innerText = title;
  heading.innerText = `What Is My ${type} Sign?`;
  paragraph.innerText = `
    If you are unsure of your ${type} sign, then use our ${type} sign calculator to look up in which constellation ${type} was located at the moment of your birth:
  `;

  formType = type;
};

const handleSubmit = async (e) => {
  e.preventDefault();
  errorContainer.style.display = "none";
  errorMessage.innerText = "";
  calBtn.disabled = true;
  calBtn.innerText = "Calculating...";

  try {
    const fname = document.getElementById("fname").value;
    const city = document.getElementById("city").value;
    const dob = document.getElementById("dob").value;
    const timeOfBirth = document.getElementById("timeOfBirth").value;
    const unknownTime = document.getElementById("unknownTime").checked;

    if (!fname || !city || !dob || (!unknownTime && !timeOfBirth)) {
      throw new Error("Please fill all fields");
    }

    const [year, month, day] = dob.split("-");
    const data = {
      name: fname,
      place_of_birth: city,
      dob: `${day}/${month}/${year}`,
      time: unknownTime ? "00:00" : timeOfBirth,
    };

    const response = await fetch(`${API_URL}/calculate_chart`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log(result);

    if (!result.planets) {
      throw new Error("Invalid API response: missing planets data");
    }

    const sign = result.planets[formType]?.sign;

    if (sign) {
      resultSign.innerText = `Your ${formType} sign is ${sign}`;
      resultSun.innerText = `Sun: ${result.planets.Sun?.sign}` || "Sun: Unknown";
      resultMoon.innerText = `Moon: ${result.planets.Moon?.sign}` || "Moon: Unknown";
      resultMercury.innerText = `Mercury: ${result.planets.Mercury?.sign}` || "Mercury: Unknown";
      resultVenus.innerText = `Venus: ${result.planets.Venus?.sign}` || "Venus: Unknown";
      resultMars.innerText = `Mars: ${result.planets.Mars?.sign}` || "Mars: Unknown";
      resultJupiter.innerText = `Jupiter: ${result.planets.Jupiter?.sign}` || "Jupiter: Unknown";
      resultSaturn.innerText = `Saturn: ${result.planets.Saturn?.sign}` || "Saturn: Unknown";
      resultUranus.innerText = `Uranus: ${result.planets.Uranus?.sign}` || "Uranus: Unknown";
      resultNeptune.innerText = `Neptune: ${result.planets.Neptune?.sign}` || "Neptune: Unknown";
      resultPluto.innerText = `Pluto: ${result.planets.Pluto?.sign}` || "Pluto: Unknown";
      resultAsc.innerText = `Ascendant: ${result.planets.Ascendant?.sign}` || "Ascendant: Unknown";

      resultContainer.style.display = "block";
      formAction.style.display = "none";
      mainContainer.style.display = "none";
      resultHeading.innerText = "Your Result:";
    } else {
      throw new Error(`Unable to determine ${formType} sign`);
    }
  } catch (error) {
    errorContainer.style.display = "block";
    errorMessage.innerText = error.message;
  } finally {
    calBtn.disabled = false;
    calBtn.innerText = "Calculate";
  }
};

const backHandler = () => {
  const isFormVisible = formContainer.style.display === "block";
  const isResultVisible = resultContainer.style.display === "block";

  if (isFormVisible) {
    if (isResultVisible) {
      resultContainer.style.display = "none";
    } else {
      formContainer.style.display = "none";
      mainContainer.style.display = "block";
    }
    errorContainer.style.display = "none";
    formAction.style.display = "block";
  }
};

formAction.addEventListener("submit", handleSubmit);