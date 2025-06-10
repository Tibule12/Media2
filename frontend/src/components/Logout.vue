<template>
  <div>
    Logging out...
  </div>
</template>

<script>
export default {
  name: 'Logout',
  mounted() {
    this.$store.dispatch('logout')
    this.$router.push('/login')
  }
}
</script>
