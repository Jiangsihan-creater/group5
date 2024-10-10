<template>
  <div
    class="w3l-signinform"
    :style="{background:'url(' +(loginBackground || require('./image/bg.jpg')) +') no-repeat center', backgroundSize: '100% 100%' }"
  >
    <!-- container -->
    <div class="wrapper">
      <!-- main content -->
      <div class="w3l-form-info">
        <!-- logo -->
        <img class="page-login--logo" :src="siteLogo" width="300"/>
        <div class="w3_info">
          <h2 style="text-align: center">{{ siteName || processTitle }}</h2>
          <el-card shadow="always" class="card">
            <el-tabs v-model="activeName">
              <el-tab-pane label="账号密码登录" name="first" stretch>
                <span slot="label"><span style="margin: 30px">账号密码登录</span></span>
                <br/>
                <el-form
                  ref="loginForm"
                  label-position="top"
                  :rules="rules"
                  :model="formLogin"
                  size="default"
                >
                  <el-form-item prop="username">
                    <el-input
                      type="text"
                      v-model="formLogin.username"
                      prefix-icon="el-icon-user-solid"
                      placeholder="用户名"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item prop="password">
                    <el-input
                      type="password"
                      v-model="formLogin.password"
                      prefix-icon="el-icon-s-promotion"
                      show-password
                      placeholder="密码"
                      @keyup.enter.native='submit'
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item
                    prop="captcha"
                    v-if="captchaState"
                    :rules="{required: true,message: '请输入验证码',trigger: 'blur'}"
                  >
                    <el-input
                      type="text"
                      v-model="formLogin.captcha"
                      placeholder="验证码"
                      @keyup.enter.native="submit"
                    >
                      <template slot="append">
                        <img
                          class="login-code"
                          style="cursor: pointer;"
                          height="33px"
                          width="145px"
                          slot="suffix"
                          :src="image_base"
                          @click="getCaptcha"
                        />
                      </template>
                    </el-input>
                  </el-form-item>
                </el-form>
                <button class="btn btn-primary btn-block" style="padding: 10px 10px;" @click="submit">
                  登录
                </button>
                <div style="text-align: right;margin-top: 8px;color: blue;">
                  <span style="cursor: pointer;" @click="register">注册</span>
                </div>
                <component v-if="componentTag" :is="componentTag"></component>
              </el-tab-pane>
            </el-tabs>
          </el-card>
          <!-- footer -->
          <div class="footer">
          </div>
          <!-- footer -->
        </div>
      </div>
      <!-- //main content -->
    </div>
    <!-- //container -->
    <register :showDialog="showDialog" :close="close"></register>
  </div>
</template>
<script>
import base from './base.vue'
import register from './register.vue'
const pluginImport = require('@/libs/util.import.plugin')
export default {
  extends: base,
  components: {
    register
  },
  name: 'page',
  data () {
    return {
      activeName: 'first',
      componentTag: '',
      showDialog:false
    }
  },
  created () {
    // 注册第三方登录插件
    var componentTag = ''
    try {
      componentTag = pluginImport('dvadmin-third-web/src/login/index')
    } catch (error) {
      componentTag = ''
    }
    this.componentTag = componentTag
  },
  mounted () {
  },
  methods: {
    register(){
      this.showDialog = true
    },
    close(){
      this.showDialog = false
    }
  }
}
</script>

<style lang="scss" scoped>
  @import './css/style.css';

  .copyrights {
    text-indent: -9999px;
    height: 0;
    line-height: 0;
    font-size: 0;
    overflow: hidden;
  }

  // 快速选择用户面板
  .page-login--quick {
    margin-top: 20px;
  }

  .page-login--quick-user {
    @extend %flex-center-col;
    padding: 10px 0px;
    border-radius: 4px;

    &:hover {
      background-color: $color-bg;

      i {
        color: $color-text-normal;
      }

      span {
        color: $color-text-normal;
      }
    }

    i {
      font-size: 36px;
      color: $color-text-sub;
    }

    span {
      font-size: 12px;
      margin-top: 10px;
      color: $color-text-sub;
    }
  }
</style>
