<template>
    <TopNav />
    <div class="container-fluid pt-5">
        <div class="text-center w-100 pt-5 pb-3">
            <h1>Your Old Transcriptions</h1>
        </div>
        <hr />
        <div v-if="old_transcriptions_flag">
            <div v-for="(value, index) in old_transcriptions">
                <div class="mb-1">
                    <span> {{ getTimeStamp(value.audio_file) }} </span>
                </div>
                <audio controls>
                    <source :src="audioURL(value.audio_file)" type="audio/mp3">
                </audio>
                <p>
                    {{ value.audio_ct }}
                </p>
                <hr />
            </div>
        </div>
        <div v-else>
            <div class="text-center w-100 pt-5 pb-3">
                <h1>No Transcriptions Found</h1>
            </div>
        </div>
    </div>
    <nav class="navbar sticky-bottom position-absolute navbar-dark bg-dark">
        <div class="container-fluid">
            <div>
                <span class="w-100 text-small">choose audio file to transcribe</span>
                <div class="input-group mb-3 pt-2">
                    <input type="file" class="form-control" id="inputGroupFile02" ref="fileInput"
                        @changeInput="handleFileInput" accept=".mp3">
                    <button class="btn bg-white btn-sm ms-2" @click="fetchTranscription" v-if="!tsFlag">Submit</button>
                </div>
            </div>
            <div v-if="tsFlag">
                <span>...getting your transcriptions</span>
            </div>
            <div class="d-flex">
                <button class='w-100 btn btn-sm m-2' type="submit" style="background-color: var(--bp-khaki);"
                    @click="record" id="startRecording">Start Recording</button>
                <button class='w-100 btn btn-sm m-2' type="submit" style="background-color: var(--bp-khaki);"
                    @click="stopRecord" id="stopRecording">Stop Recording</button>
                <audio id="player" controls v-show="false"></audio>
            </div>
        </div>
    </nav>
</template>
<script>
import TopNav from '@/components/TopNav.vue';
export default {
    name: 'Dashboard',
    components: {
        TopNav
    },
    data: function () {
        return {
            recorder: null,
            old_transcriptions: null,
            files: [],
            transcription: "",
            tsFlag: false,
        }
    },
    async mounted() {
        const headers = { 'Content-Type': 'application/json', "Authorization": "Bearer " + localStorage.getItem("access_token") };
        await fetch(__BACKEND_URL__ + localStorage.getItem("username") + '/get_transcriptions', { headers: headers, method: "GET" })
            .then(response => {
                return response.json();
            }).then(data => { if (!data.detail) { this.old_transcriptions = data.reverse() } else { this.$router.push('/logout') } });

    },
    computed: {
        old_transcriptions_flag: function () {
            if (JSON.parse(JSON.stringify(this.old_transcriptions)) != 'Invalid credentials') {
                return true;
            }
            else {
                return false;
            }
        },
    },
    methods: {
        getTimeStamp(fileName) {
            let ret_str = ''
            let temp = fileName.slice(0, 19).split('_');
            ret_str = temp[3] + ':' + temp[4] + ' ' + temp[2] + '/' + temp[1] + '/' + temp[0];
            return ret_str;
        },
        record: async function () {
            if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
                //Feature is not supported in browser
                //return a custom error
                let msg = 'mediaDevices API or getUserMedia method is not supported in this browser,';
                let msg2 = 'sorry you can\'t use this application in this browser, please use a modern browser like Chrome or Firefox';
                alert(msg + msg2);
            }

            let mediaStreamObj = await navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
                return stream;
            }).then(data => { return data }).catch(function (err) {
                alert("microphone access denied");
            });

            this.recorder = new MediaRecorder(mediaStreamObj);
            console.log(this.recorder.state)


            this.recorder.start();
            console.log(this.recorder.state);
        },
        stopRecord: function () {
            if (this.recorder) {
                this.recorder.stop();
                console.log(this.recorder.state);
                this.tsFlag = true;

                let da = [];
                // If audio data available then push 
                // it to the chunk array
                this.recorder.ondataavailable = function (ev) {
                    da.push(ev.data);
                }

                // Convert the audio data in to blob 
                // after stopping the recording
                this.recorder.onstop = async function (ev) {

                    // blob of type mp3
                    let audioData = new Blob(da,
                        { 'type': 'audio/mp3;' });

                    // After fill up the chunk 
                    // array make it empty
                    da = [];

                    // Creating audio url with reference 
                    // of created blob named 'audioData'
                    let audioSrc = window.URL
                        .createObjectURL(audioData);

                    let audio = document.getElementById('player');

                    // Pass the audio url to the 2nd video tag
                    audio.src = audioSrc;
                    await fetch(audioSrc).then(res => res.blob()).then(async (blob) => {
                        const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token") };
                        const data = new FormData();
                        data.append('file', blob, 'recorded_audio.mp3');
                        await fetch(__BACKEND_URL__ + 'get_transcription', { headers: headers, method: "POST", body: data })
                            .then(response => {
                                return response.json();
                            }).then((data) => {
                                let res_data = data;
                                let res_obj = {
                                    "username": localStorage.getItem("username"),
                                    "audio_ct": res_data["transcription"],
                                    "audio_file": res_data["audio_file"]
                                }
                                location.reload();
                            });
                    }).catch(error => {
                        console.log(error)
                    });
                }
                this.recorder = null;
            }
        },
        audioURL: function (audio_file) {
            return __BACKEND_URL__ + 'static/' + audio_file;
        },
        handleFileInput() {
            const fileInput = this.$refs.fileInput;
            const files = fileInput.files;
        },
        async fetchTranscription() {
            this.tsFlag = true;
            const fileInput = this.$refs.fileInput;
            const files = fileInput.files;
            if (files.length > 0) {
                const selectedFile = files[0];
                if (selectedFile) {
                    let formData = new FormData();
                    formData.append("file", selectedFile);
                    const headers = { "Authorization": "Bearer " + localStorage.getItem("access_token"), 'accept': 'application/json' };
                    await fetch(__BACKEND_URL__ + 'get_transcription', { method: "POST", body: formData, headers: headers })
                        .then((response) => {
                            return response.json();
                        }).then((data) => {
                            let res_data = data;
                            let res_obj = {
                                "username": localStorage.getItem("username"),
                                "audio_ct": res_data["transcription"],
                                "audio_file": res_data["audio_file"]
                            }
                            if (res_data["transcription"]) {

                                if (this.old_transcriptions.length > 0) {
                                    this.old_transcriptions = [res_obj, ...this.old_transcriptions]
                                }
                                else {
                                    this.old_transcriptions = [res_obj]
                                }
                                location.reload();
                            }
                        })
                        .catch(error => {
                            console.log(error)
                        });
                }
            }
            this.tsFlag = false;
        },
    }
}

</script>
