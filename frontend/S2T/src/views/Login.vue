<template>
    <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5">
      <h1 style="color:var(--maize);" class="text-center">Log in to S2T</h1>
      <br>
      <form method="POST" @submit.prevent="handleFormSubmit">
        <div class="form-floating mb-3">
          <input type="text" :class='{ "form-control": true, "is-invalid": v$.username.$error }' v-model="username"
            name="username" id="floatingInput" placeholder="username" autocomplete="off">
          <label for="floatingInput">username</label>
          <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.username.$error">
            <span>{{ v$.username.$errors[0].$message }}</span>
          </div>
        </div>
        <div class="form-floating mb-3">
          <input type="password" :class='{ "form-control": true, "is-invalid": v$.password.$error }' v-model="password"
            name="password" id="floatingPassword" placeholder="Password" autocomplete="off">
          <label for="floatingPassword">Password</label>
          <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.password.$error">
            <span>{{ v$.password.$errors[0].$message }}</span>
          </div>
        </div>
        <button class="w-100 btn btn-lg" type="submit"
          style="background-color: var(--bp-khaki); color: var(--bp-white);">Sign in</button>
        <hr class="my-4">
        <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errStatus">
          <strong>{{ errormsg }}</strong>.
          <button type="button" class="btn-close" aria-label="Close" @click="errStatus = false"></button>
        </div>
        <small>New to Pixel Shows? <router-link to="/signup">Sign up now</router-link> </small>
      </form>
    </div>
  </template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, alphaNum, helpers, minLength, maxLength } from '@vuelidate/validators'
export default {
  setup() {
    return {
      v$: useVuelidate()
    }
  },
  name: 'UserLogin',
  data: function () {
    return {
      username: '',
      password: '',
      errormsg: '',
      errStatus: false
    }
  },
  validations: {
    username: {
      required: helpers.withMessage('The username field is required', required),
      alphaNum: helpers.withMessage('The username must contain only letters and numbers', alphaNum),
      minLength: helpers.withMessage('The username should be minimum of 3 characters and maximum of 20 characters',minLength(3)),
      maxLength: helpers.withMessage('The username should be minimum of 3 characters and maximum of 20 characters',maxLength(20)),
    },
    password: { required: helpers.withMessage('The password field is required', required) }
  },
  methods: {
    handleFormSubmit: async function () {
      this.v$.$touch()
      if (!this.v$.$error) {
        const headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        const formdata = new URLSearchParams();
        formdata.append('username', this.username)
        formdata.append('password', this.password)
        console.log(formdata)
        await fetch(__BACKEND_URL__ + "login", { headers: headers, body: formdata, method: "POST" })
          .then(response => {
            console.log(response);
            return response.json();
          })
          .then(async (data) => {
            console.log(data)
            if (data.access_token) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("username", this.username);
              localStorage.setItem("exp_time", data.exp_time);
              this.$router.push('/dashboard');
            }
            else {
              this.errStatus = true;
              throw new Error(data.detail);
            }
          })
          .catch((error) => {
            this.errormsg = error;
            console.log(error)
          })
      }
    }
  }
}
</script>
  
<style></style>