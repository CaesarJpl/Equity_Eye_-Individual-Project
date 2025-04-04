<template>
    <div class="start-page">
      <div class="content">
        <h1>Equity Eye</h1>
        <p class="subtitle">
          A personalized<br />
          Portfolio tracking tool<br />
          and<br />
          Financial news platform
        </p>
        <div class="buttons">
          <router-link to="/login">
          <button class="login-button">Log in</button>
          </router-link>
          <router-link to="/register">
          <button class="register-button">Register</button>
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "StartPage",
  };
  </script>
  
  <style scoped>
  .start-page {
    display: flex;
    height: 100vh;
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
    align-items: center;
    justify-content: center;
  }
  
  .content {
    width: 100vw; 
    height: 100vh; 
    max-width: 1500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    justify-content: center; 
    align-items: center; 
  }
  
  h1 {
    display: flex;
    width: 365.533px;
    height: 104.643px;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #000;
    text-align: center;
    text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    font-family: Inter;
    font-size: 91.772px;
    font-style: normal;
    font-weight: 300;
    line-height: 121.029%;
    margin-top: -50px; /* 向上移动 20px，值可以根据需求调整 */
  }
  
  .subtitle {
    display: flex;
    width: 755.857px;
    height: 380.969px;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #702525;
    text-align: right;
    text-shadow: 0px 4px 8px rgba(0, 0, 0, 0.25);
    font-family: Inter, sans-serif;
    font-size: 65px;
    font-style: normal;
    font-weight: 100;
    line-height: normal;
    margin-top: 1rem;
    margin-left: auto;  
  }
  
  .buttons {
    display: flex;
    justify-content: center;
    gap: 5rem;
    margin-top: 2rem;
  }
  
  button {
    width: 284.112px;
    height: 100.546px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: none;
    border-radius: 32px;
    background: #D9D9D9;
    color: #4a4a4a; /* 设置按钮文字颜色 */
    cursor: pointer;
    flex-shrink: 0; /* 防止按钮在 Flex 布局下缩小 */
  }

  .login-button {
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #345484;
    text-align: center;
    font-family: Inter;
    font-size: 40px;
    font-style: normal;
    font-weight: 300;
    line-height: normal;
  }
  
  .register-button {
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex-shrink: 0;
    color: #996921;
    text-align: center;
    font-family: Inter;
    font-size: 40px;
    font-style: normal;
    font-weight: 300;
    line-height: normal;
  }
  .start-page a {
  text-decoration: none;
}
  </style>