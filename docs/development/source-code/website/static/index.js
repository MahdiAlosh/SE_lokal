const dropdown_liste = document.getElementById("dropdown_container");
const searchForm = document.getElementById("searchForm");
const companyName = document.getElementById("companyName");
const dropdown_container = document.getElementById("dropdown_container")

let inFetch = false;

async function updateInputValue(value) {
  dropdown_liste.textContent = null;
  if(value){
    if(!inFetch){
      dropdown_container.style.display = "block";
      inFetch = true;
      await fetchData(value);
      inFetch = false;
    }
  }else{
    dropdown_container.style.display = "none";
  }
}

async function fetchData(value){
  await fetch(`https://de.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit=5&gsrsearch='${value}'`, {
      //  limit = 5; Anzahl der vorgeschlagene Ergebnisse 
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name:value
      })
  })
  .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
  })
  .then((data) => {
      if(data.query && data.query.pages){
        const fetchPages = data.query.pages;
        Object.entries(fetchPages).forEach(([key, value]) => {
            const container = document.createElement("div");
            container.classList.add("dropdown_list");
            container.textContent = value.title;
            container.onclick = () =>{
              companyName.value = value.title;
              searchForm.submit();
            }
            dropdown_liste.append(container);
        });
      }else{
        const container = document.createElement("div");
        container.textContent = "No Data";
        dropdown_liste.append(container);
      }
  })
  .catch((error) => {
      //this.$root.$refs.NavComRef.msg(error.message);
      console.log(error)
  });
}

