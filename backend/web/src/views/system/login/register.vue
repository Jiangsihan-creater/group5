<template>
  <div v-if="showDialog">
    <el-dialog title="用户注册" :visible.sync="showDialog"  width="500px" append-to-body :close-on-click-modal="false" @close="close">
    <el-form :model="form" :rules="rules" ref="ruleForm">
      <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
        <el-input v-model="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="用户名" :label-width="formLabelWidth" prop="username">
        <el-input v-model="form.username" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
        <el-input v-model="form.password" autocomplete="off"></el-input>
      </el-form-item>
      <!-- <el-form-item label="活动区域" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="请选择活动区域">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
          </el-select>
        </el-form-item> -->
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="submit">确 定</el-button>
    </div>
  </el-dialog>
  </div>
</template>
<script>
// import * as api from './api'
// import * as api from '../user/api'
import * as api from './api2'
export default {
  name: 'register',
  props: {
    showDialog: Boolean,
    close: Function
  },
  data() {
    return {
      form: {
        name: '',//姓名
        dept: 3,
        is_active: true,
        role: [2],
        username: '',//用户名
        password: ''
      },
      formLabelWidth: '80px',
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ],
      }
    }
  },
  created() {

  },
  mounted() {
  },
  methods: {
    submit() {
      const that = this
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          const addForm = {
            name:that.form.name,
            username:that.form.username,
            password:that.$md5(that.form.password),
            dept: that.form.dept,
            is_active: that.form.is_active,
            role: that.form.role,
          }
          // api.Register(addForm).then(res => {
          //   if(res.code==2000){
          //     that.$message.success(res.msg)
          //   }
          //   that.form = {}
          //   that.close()
          // }).catch((err) => {
          // })
          api.AddObj(addForm).then(res => {
            if(res.code==2000){
              that.$message.success(res.msg)
            }
            that.form = {}
            that.close()
          }).catch((err) => {
          })
        } else {
          return false;
        }
      });
    },
  }
}
</script>

<style scoped></style>
