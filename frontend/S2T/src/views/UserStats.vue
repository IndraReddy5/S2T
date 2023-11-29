<template>
    <TopNav />
    <div class="container-fluid pt-5">
        <div class="pt-5 text-center">
            <div v-if="userTopPhrases.length > 0">
                <h3>Your Top Phrases</h3>
                <div v-for="(value) in userTopPhrases">
                    <p> {{value}} </p>
                </div>
            </div>
            <h3>Most Frequently Used Words on this Application by all Users</h3>
            <div class="d-flex text-center">
                <table class="table table-sm table-dark pt-2">
                    <thead>
                        <tr>
                            <th scope="col">Word</th>
                            <th scope="col">Frequency</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="value in freqWords">
                            <td>{{ value.word }}</td>
                            <td>{{ value.frequency }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-if="userTopWords.length > 0" class="pt-3">
                <h3>Most Frequent words used by you</h3>
                <div class="d-flex w-100">
                    <table class="table table-sm table-dark pt-2">
                        <thead>
                            <tr>
                                <th scope="col">Word</th>
                                <th scope="col">Frequency</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="value in userTopWords">
                                <td>{{ value.word }}</td>
                                <td>{{ value.frequency }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import TopNav from '@/components/TopNav.vue'
export default {
    components: {
        TopNav
    },
    data: function () {
        return {
            userTopWords: [],
            userTopPhrases: [],
            freqWords: [],
        }
    },
    mounted() {
        this.getTopWords();
        this.getTopPhrases();
        this.getFreqWords();
    },
    methods: {
        async getTopWords() {
            const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token"), 'accept': 'application/json' };
            await fetch(__BACKEND_URL__ + localStorage.getItem("username") + '/top_words', { method: "GET", headers: headers })
                .then((response) => {
                    return response.json();
                }).then((data) => { this.userTopWords = data }).catch(error => {
                    console.log(error)
                });
        },
        async getTopPhrases() {
            const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token"), 'accept': 'application/json' };
            await fetch(__BACKEND_URL__ + localStorage.getItem("username") + '/top_phrases', { method: "GET", headers: headers })
                .then((response) => {
                    return response.json();
                }).then((data) => { this.userTopPhrases = data.transcriptions }).catch(error => {
                    console.log(error)
                });
        },
        async getFreqWords() {
            const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token"), 'accept': 'application/json' };
            await fetch(__BACKEND_URL__ + 'top_words', { method: "GET", headers: headers })
                .then((response) => {
                    return response.json();
                }).then((data) => { this.freqWords = data }).catch(error => {
                    console.log(error)
                });
        }
    }
}
</script>