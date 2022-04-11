<template>

<form @submit.prevent="uploadPhoto" id="uploadForm">
    <span id="message" class="alert form-control hide"></span>
 <div class="container">
     <label for="description">Description</label>
     <textarea id="description" name="description" rows="3" cols="150"></textarea>
     <label for="photo">Photo Upload</label>
     <br>
     <input type="file" id="photo" name="photo">
     <br><br>
     <input type="submit" name="submit" class="btn btn-primary">
     </div>
 </form>
 
      
</template>

<script>
export default { 
    data() {
        return {
            csrf_token: ''
            };
    },
    methods: {
    uploadPhoto(){
        let uploadForm = document.getElementById('uploadForm');
        let form_data = new FormData(uploadForm);
        let messagecontainer= document.querySelector('#message');
    fetch("/api/upload", 
    {method: 'POST', 
    body: form_data,
    headers: {
        'X-CSRFToken': this.csrf_token
        }})
    .then(function (response) {return response.json();})
    .then(function (data) {
        if (Array.isArray(data)){
          messagecontainer.innerHTML='';
          let errors = data;
          for (let err=0; err<errors.length; err++){
                    const errElem = document.createElement("li");
                    const node = document.createTextNode(errors[err]);
                    errElem.appendChild(node);
                    messagecontainer.appendChild(errElem);
                }
            messagecontainer.classList.remove('show');
            messagecontainer.classList.add('alert-danger');
            messagecontainer.classList.remove('alert-success');
            messagecontainer.classList.add('show');
        }
        else {
            messagecontainer.classList.remove('show');
            messagecontainer.classList.add('alert-success');
            messagecontainer.classList.remove('alert-danger');
            messagecontainer.classList.add('show');
            messagecontainer.innerHTML= data.message;
        }

 // display a success message
 console.log(data);})
 .catch(function (error) 
 {console.log(error);
 });
 },
 getCsrfToken() {
     let self = this;
     fetch('/api/csrf-token')
    .then((response) => response.json())
        .then((data) => {console.log(data);
        self.csrf_token = data.csrf_token;
 })
 }
},
created() {
 this.getCsrfToken();
},
 }

</script>

<style>
form *{
    margin-top: 1em;
}
.hide {
    display: none;
}
.show{
    display: block;
}
/* Add any component specific styles here */
</style>
