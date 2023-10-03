<template>
   
        <div class="searchbar">
      <input  v-model="searchTerm" placeholder="Testfile.txt">
      <button src="../assets/search-svgrepo-com.svg" @click="search">Buscar</button>
        </div>
  
      <div v-if="downloadLink" class="download-link">
      <h2 >Download File:</h2>
      <a :href="downloadLink" :download="downloadFileName"> {{downloadFileName}}</a>
    </div>
  
    <h3 v-if="showError ==  true" class="error-msg">File not found</h3>

  </template>
  
  <script>
  import axios from 'axios';
  
  export default {

    data() {
      return {
        searchTerm: '',
        downloadLink: null,
        downloadFileName: null,
        showError: null,
        errorMessage: ''
      };
    },
    methods: {
      search() {
        const apiUrl = `http://localhost/readfile`;
  
        axios.post(apiUrl,{"file":this.searchTerm}, { responseType: 'arraybuffer' })
        .catch((error)=>{
          this.showError = true;
            console.log(error)
            
        })
        .then((response) => {
            

            const blob = new Blob([response.data], { type: 'application/octet-stream' });

          const url = window.URL.createObjectURL(blob);
            //this.searchResults = response;
            this.downloadFileName = this.searchTerm;
            this.downloadLink = url;  
            this.showError = false;
        })


      },
    },
  };
  </script>
<style scoped>
    @import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

.error-msg{
  display: flex;
  justify-content: center;
  color: red;
}
    
.searchbar{
    display: flex;
    justify-content: center;
    
}

.download-link{
    display: flex;
    justify-content: center;

}
.download-link h2{
  margin-right: 10px;
}
.download-link a{
  
  color: darkgreen;
  font-size: x-large;
  
}

input {
  
  width: 600px;
  
  padding: 10px 45px;
  background: white ;
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

button{
    padding: 10px 5px;
    font-size: 16px;
    background: white  ;
    border: none;
 
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}



.error {
  background-color: #FEE;
  border: 1px solid #EDD;
  color: #A66;
}
</style>