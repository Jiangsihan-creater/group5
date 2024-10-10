<template>
   <el-card class="box-card" style="margin: 10PX;width: 800px;overflow-y: auto"  v-loading="loading"
    element-loading-text="邮件内容预测中..."
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)">
      <div style="margin-top: 0px;">选择要判定的文件</div>
        <!--     文件     -->
      <div style="margin-top: 10px;">
          <el-upload
            :action="uploadUrl"
            :headers="uploadHeaders"
            :on-change="handleChange"
            :on-success="handleUploadSuccess"
            :on-exceed="handleUploadExceed"
            :file-list="fileList"
            :limit="1"
            accept=".csv"
          >
          <el-button size="small" type="primary">选择文件</el-button>
          </el-upload>
        </div>

        <div style="margin-top: 40px;position: relative;">邮件内容：
          <el-button style="position: absolute;right: 200px;top: -20px;" type="success" @click="onSubmit">点击识别</el-button>
        </div>
        <div style="width: 600px;height: 260px;margin-top: 8px;border: 1px solid #ddd;padding: 6px;overflow-y: auto;" v-html="mailContent">

        </div>
        <div style="margin-top: 20px;">判断结果：</div>
        <div style="width: 600px;height: 260px;margin-top: 8px;border: 1px solid #ddd;padding: 6px;overflow-y: auto;" v-html="mailContentResult">
        </div>
    </el-card>

</template>

<script>

import * as api from './api'
import util from '@/libs/util'


export default {
  name: 'Test',
  components: {

  },
  data () {
    return {
      uploadUrl: util.baseURL() + 'api/system/file/',
      uploadHeaders: {
        Authorization: 'JWT ' + util.cookies.get('token')
      },
      fileList:[],
      setting:{
        id:14,
        value:'',
        key:'models_params',
        title:'模型参数'
      },
      uploadFile:{
        id:'',
        name:'',
        size:'',
        url:''
      },
      loading:false,
      inputContent:'',
      mailContent:'',
      mailContentResult:'',

    }
  },
  methods: {
    handleUploadSuccess(response, file, fileList){
      console.log('file',file)
      console.log('response',response)
      const {id,name,size,url} = response.data
      this.uploadFile = {
        id,name,size,url
      }
      this.getDataContent()
    },
    handleChange(file, fileList) {
    },
    handleUploadExceed(files, fileList){
      this.$message.warning('最多只能上传一个文件，如果更新文件请先删除原文件')
    },
    onSubmit () {
      if(!this.uploadFile.id){
        this.$message.warning('请先上传数据集')
        return
      }
      this.loading = true
      api.Test(this.uploadFile.url).then(res => {
            // this.$message.success('保存成功')
            // this.loading = true
            this.loading = false
            const resultList = res.data
            const tempResult = []
            resultList.forEach((item,index) => {
              const text = this.inputContent[index]
              tempResult.push(`${text}-----预测结果：<span style="color:red">${item}</span>`)
            })
            this.mailContentResult = tempResult.join('<br>')
        })
    },
    getDataContent(){
      this.mailContent = ''
      api.GetDataContent(this.uploadFile.url).then(res => {
        console.log('@content',res)
          //  this.mailContent = res.data.join('\r\n')
          this.inputContent = res.data
          this.mailContent = res.data.join('<br>')
        })
    }
  },
  created () {
  }
}
</script>

<style scoped>

</style>
