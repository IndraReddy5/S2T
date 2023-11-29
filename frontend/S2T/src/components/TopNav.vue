<template>
    <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark">
        <div class="container-fluid d-flex justify-content-center">
            <div>
                <a class="navbar-brand" href="/dashboard">S2T</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item dropdown" role="search">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            {{ username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-dark">
                            <li><router-link class="dropdown-item" to="/insights">insights</router-link></li>
                            <li><a class="dropdown-item" href="/logout">logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script>
import { RouterLink } from 'vue-router';

export default {
    name: 'TopNav',
    data() {
        return {
            username: localStorage.getItem('username'),
        };
    },
    mounted() {
        this.getExpTimeInterval()
        this.refreshTokenInterval = setInterval(() => {
            this.getRefreshToken();
        }, this.refreshTime * 60 * 1000);
    },
    beforeUnmount() {
        clearInterval(this.refreshTokenInterval);
    },
    methods: {
        async getRefreshToken() {
            const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token"), "Content-Type": "application/json" };
            await fetch(__BACKEND_URL__ + 'get_token', { headers: headers, method: "GET" })
                .then(response => {
                    return response.json();
                }).then((data) => {
                    if ((data.exp_time > 10)) {
                        localStorage.setItem("access_token", data.access_token);
                        localStorage.setItem("exp_time", data.exp_time);
                        localStorage.setItem("last_token_accessed_time", new Date().toUTCString());
                        clearInterval(this.refreshTokenTimeInterval);
                        this.refreshTokenInterval = setInterval(() => {
                            this.getRefreshToken();
                            console.log("test");
                        }, (data.exp_time - 5) * 60 * 1000);
                    }
                }).catch(error => {
                    console.log(error);
                });
        },
        async getExpTimeInterval() {
            this.expTimeInterval = localStorage.getItem("exp_time");
            this.lastAccessTime = localStorage.getItem("last_token_accessed_time");
            let now = new Date(Date.now());
            let tokenExpiryLimit = new Date(this.lastAccessTime);
            tokenExpiryLimit.setMinutes(tokenExpiryLimit.getMinutes() + parseInt(this.expTimeInterval) - 5);
            this.refreshTime =  Math.max( 1, Math.round((tokenExpiryLimit - now)/(1000*60)));
        }
    },
    components: { RouterLink }
}
</script>