<template>
    
        <div class="navbar"> 
            <div class="main">
              <h1 class="header"><router-link to="/">Pentagram</router-link></h1>
                <div>
                    <router-link to="/login" class="buttonStyle">Login/Register</router-link>
                </div>
                <div>
                  <router-link to="/post" class="buttonStyle">Create Post</router-link>
              </div>
              
            </div>
            
          </div>
    
</template>

<script>
    export default {
        
    }
</script>

<style src="../styles/navbar.css" scoped>
</style>