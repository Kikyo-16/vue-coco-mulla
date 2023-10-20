<template>
   <audio ref="player" :src="musicSrc"  controls preload="auto"
          @play="play()"></audio>
</template>

<script>
export default {
  name: 'MyAudio',
  props: {
    musicSrc: {
      type: String,
      require: true
    },
    audioTag:{
      type: Array,
      require: true
    }

  },
  watch(){

  },
  data(){
    return {
    }
  },
  mounted() {
    let this_t = this;
    setInterval(function (){
      this_t.timeupdate();
    }, 10);
  },
  methods:{
    play(){
      this.$emit('play');
    },
    getProgress(){
      if(this.$refs.player=== null) {
        return [0, 0, 1];
      }
      return [this.$refs.player.currentTime/this.$refs.player.duration,
          this.$refs.player.currentTime,
          this.$refs.player.duration];
    },
    timeupdate(){
      //console.log(this.$refs.player);
      if(this.$refs.player !== null &&!this.$refs.player.paused) {
        this.$emit('timeupdate', this.getProgress(), this.audioTag);
      }
    },
    pause(){
      if(this.$refs.player !== null && !this.$refs.player.paused){
        this.$refs.player.pause();
      }
    },
    continue(ratio){
      if(this.$refs.player=== null){
        return;
      }
      // eslint-disable-next-line no-empty
      if( this.$refs.player.paused){

      }else{
        this.$refs.player.pause();
      }
      this.$refs.player.currentTime = ratio * this.$refs.player.duration;
      this.$refs.player.play();
    },
  }
}
</script>
