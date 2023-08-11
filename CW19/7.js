const student = {
  firstName: "ali",
  lastName: "dana",
  age: 20,
  skills: ["JS", "python", "react"],
  country: "Iran",
  enrolled: true
};

localStorage.setItem("student", JSON.stringify(student));

const retrievedStudent = JSON.parse(localStorage.getItem("student"));
console.log(retrievedStudent);
