function updateInputValue(value) {
  userInput = value;
  console.log(userInput); // Hier kannst du die Eingabe in der Konsole anzeigen
}


function submitForm() {
  var companyName = document.getElementById("companyName").value;
  if (companyName.trim() !== "") {
    document.getElementById("searchForm").submit();
  } else {
    alert("Please enter a valid company name.");
  }
}