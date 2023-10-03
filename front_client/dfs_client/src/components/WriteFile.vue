<template>
  <div class="container">
    <div class="input-group">
      <input style="margin-left: 3rem;" type="file" ref="fileInput" @change="handleFileChange">
      <h3>Carpeta</h3>
      <input style="width: 250px;" type="text" v-model="folder" placeholder="Dejar vacio para guardar en la raiz">
    </div>
    <div class="input-group">
      <label>
        <h3>Crear directorio</h3>
        <input type="checkbox"  v-model="createFolder"> 
      </label>
      <input
        type="text"
        v-model="createFolderName"
        v-if="createFolder"
        placeholder="Nombre del directorio"
        style="margin-left: 10px"
      >
    </div>
    <button @click="uploadFile" class="upload-button">Subir</button>
    <h2 v-if="write_success" class="success-message">Archivo subido correctamente</h2>
    <h2 v-if="errormsg" class="error-message">Error subiendo el archivo: {{ errormsg }}</h2>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      folder: '',
      write_success: false,
      errormsg: null,
      createFolder: false, // Variable para rastrear el estado del checkbox
      createFolderName: ''
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      if (!this.selectedFile) {
        alert('Please select a file to upload.');
        return;
      }

      const formData = new FormData();
      if(this.createFolder == false){
        formData.append('create_folder','');
      }
      else{
        formData.append('create_folder',this.createFolderName);
      }
      formData.append('folder', this.folder);
      formData.append('file_data', this.selectedFile);

      console.log(formData);
      axios
        .post('http://localhost/writefile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          console.log(response.data);
          this.write_success = true;
        })
        .catch((error) => {
          // Handle errors
          console.error('Error uploading file:', error);
          this.errormsg = error;
        });
    },
  },
};
</script>
<style scoped>

.container {
  padding: 20px;
  display: grid;
  text-align: center;
}


.input-group {
  margin-bottom: 10px;
}
.input-group input {
padding: 10px;
margin: auto;
}
.upload-button {
  background-color: #00bd7e;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #027b52;
}

.success-message {
  color: green;
}

.error-message {
  color: red;
}



</style>
