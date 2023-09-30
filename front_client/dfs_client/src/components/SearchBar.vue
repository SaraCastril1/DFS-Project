

<template>
    <div>
        <div class="searchbar">
      <input  v-model="searchTerm" placeholder="Testfile.txt">
      <button src="../assets/search-svgrepo-com.svg" @click="search">Buscar</button>
        </div>
  
      <div v-if="downloadLink" class="download-link">
      <h2>Download File</h2>
      <a :href="downloadLink" :download="downloadFileName">Download {{downloadFileName}}</a>
    </div>
    </div>


  </template>
  
  <script>
  import axios from 'axios';
  import VueBasicAlert from 'vue-basic-alert'
  
  export default {
    components:{
        VueBasicAlert
    },
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
            console.log(error)
            
        })
        .then((response) => {
            

            const blob = new Blob([response.data], { type: 'application/octet-stream' });

          const url = window.URL.createObjectURL(blob);
            //this.searchResults = response;
            this.downloadFileName = this.searchTerm;
            this.downloadLink = url;  
        })

      },
    },
  };
  </script>
<style>
    @import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

.searchbar{
    display: flex;
    justify-content: center;
    
}

.download-link{
    display: flex;
    justify-content: center;

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



.alert {
  position: relative;
  top: 10;
  left: 0;
  width: auto;
  height: auto;
  padding: 10px;
  margin: 10px;
  line-height: 1.8;
  border-radius: 5px;
  cursor: hand;
  cursor: pointer;
  font-family: sans-serif;
  font-weight: 400;
}

.alertCheckbox {
  display: none;
}

:checked + .alert {
  display: none;
}

.alertText {
  display: table;
  margin: 0 auto;
  text-align: center;
  font-size: 16px;
}

.alertClose {
  float: right;
  padding-top: 5px;
  font-size: 10px;
}

.clear {
  clear: both;
}

.info {
  background-color: #EEE;
  border: 1px solid #DDD;
  color: #999;
}

.success {
  background-color: #EFE;
  border: 1px solid #DED;
  color: #9A9;
}

.notice {
  background-color: #EFF;
  border: 1px solid #DEE;
  color: #9AA;
}

.warning {
  background-color: #FDF7DF;
  border: 1px solid #FEEC6F;
  color: #C9971C;
}

.error {
  background-color: #FEE;
  border: 1px solid #EDD;
  color: #A66;
}
</style>