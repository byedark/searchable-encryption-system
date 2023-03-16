<template>
  <div class="user-information">
    <div class="one">
      <el-row class="tac">
        <el-col :span="12">
          <h2>欢迎来到个人中心</h2>
          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose">
            <!-- 第一个板块 -->
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-location"></i>
                <span>个人信息</span>
              </template>
              <el-menu-item-group>
                <template slot="title">你好，{{ title }}</template>
                <el-menu-item index="1-1">用户名：{{ username }}</el-menu-item>
                <el-menu-item index="1-1">修改密码</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <!-- 第二个板块 -->
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-document"></i>
                <span>密钥管理</span>
              </template>
              <el-menu-item-group>
                <template slot="title">存储在您设备中的密钥：</template>
                <el-menu-item index="1-1">
                  管理我的密钥
                </el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <!-- 第三个板块 -->
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-setting"></i>
                <span>设置</span>
              </template>
              <el-menu-item-group>
                <template slot="title">管理您的登录状态</template>
                <el-menu-item index="1-1">
                  <p class="button1" long type="primary" size="large" @click="logout" :disabled="logouting || logout_wait">退出登录</p>
                </el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-col>
      </el-row>
    </div>
    <!-- <div class="two">
      <div class="block">
        <el-carousel height="150px">
          <el-carousel-item v-for="item in 4" :key="item">
            <h3 class="small">{{ item }}</h3>
          </el-carousel-item>
        </el-carousel>
      </div>
    </div> -->
  </div>
</template>

<script>
import config from "../config.json";
import {decode} from "../byte_str.js";

export default {
  name:"OwnerInformation",
  data:function(){
    return {
      username:null,
      password:null,
      token:null,
      logouting:false,
      logout_wait:false,
      loaded:false,
      attributes:[],
      error_info:"",
      secret:null,
      wait_copy:false,
      pre_secret:"",
      wait_change_secret:false,
      modal:false,
      modal_delete:false,
      value1: null,
      value2: null,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'] 
    }
  },
  props:{
    title:{
      type:String,
      default:"数据使用者"
    },
    attribute:{
      type:Boolean,
      default:true
    },
    get_secret:Boolean
  },
  computed:{
    information:function(){
      if(this.error_info!="")
        return this.error_info;
      else if(this.attributes.length<=0)
        return "暂无";
      return null;
    }
  },
  watch:{
    // 更新密钥
    get_secret:function(newValue)
    {
      if(!newValue)
        return;
      
      if(localStorage.getItem("secret"))
        this.secret = localStorage.getItem("secret");
      
      this.$emit("update:get_secret",false);
    }
  },
  created:function(){
    // 必要参数
    // let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    // this.token = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    // regex = /.*searchable_encryption_username=([^;.]*).*$/; // 用于从cookie中匹配username值
    // this.username = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    // regex = /.*searchable_encryption_password=([^;.]*).*$/; // 用于从cookie中匹配username值
    // this.password = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    this.token = null;
    this.password = localStorage.getItem("password");
    this.username = localStorage.getItem("username");

    // 从设备中查看是否存在密钥
    if(localStorage.getItem("secret"))
      this.secret = localStorage.getItem("secret");

    // 首先判断是否需要获取
    if(this.attribute == false)
    {
      this.loaded=true;
      return;
    }
    let formData = new FormData();
    formData.append("username",this.username);
    formData.append("password",this.password);
    fetch(config.get_own_attribute,{
      method:"POST",
      body:formData,
      headers:{
        "X-CSRFToken":this.token
      }
    }).then(function(response){
      return response.json();
    }).then((json) => {
      if(json.status==config.success)
        this.attributes = json.attributes;
      else
        this.error_info = json.information;
      this.loaded=true;
    }).catch((error)=>{
      this.error_info = error;
      this.loaded=true;
    });
  },
  methods:{
    logout:function(){
      // 2s之后才可以再次点击
      this.logout_wait=true;
      setTimeout(()=>{
        this.logout_wait=false;
      },2000);
      this.logouting=true;
      const msg = this.$Message.loading({
        content: '正在登出...',
        duration: 0
      });
      let formData = new FormData();
      formData.append("username",this.username);
      formData.append("password",this.password);
      fetch(config.logout,{
        method:"POST",
        body:formData,
        headers:{
          "X-CSRFToken":this.token
        }
      }).then(function(response){
        return response.json();
      }).then((json) => {
        msg();
        this.logouting=false;
        if(json.status==config.success)
        {
          localStorage.removeItem("username");
          localStorage.removeItem("password");
          this.$Message.success({
            content: '登出成功',
            duration: 2
          });
          // 跳转到登录界面
          this.$router.push({name:"login"});
        }
        else
        {
          this.$Message.error({
            content: `登出失败:${json.information}`,
            duration: 2
          });
        }
      }).catch((error)=>{
        msg();
        this.logouting=false;
        this.$Message.error({
          content: `登出失败:${error}`,
          duration: 2
        });
      });
    },
    copy_success:function()
    {
      this.$Message.success({
        content:"复制成功",
        duration:2
      });
    },
    copy_error:function()
    {
      this.$Message.error({
        content:"复制失败",
        duration:2
      });
    },
    start_wait_copy:function()
    {
      // 2s之后才可以再次点击
      this.wait_copy=true;
      setTimeout(()=>{
        this.wait_copy=false;
      },2000);
    },
    change_secret:function()
    {
      // 2s之后才可以再次点击
      this.wait_change_secret=true;
      setTimeout(()=>{
        this.wait_change_secret=false;
      },2000);
      if(this.pre_secret == "")
      {
        this.$Message.error({
          content:"不能为空",
          duration:2
        });
        return;
      }
      let secret = this.check_secret();
      if(secret == false)
      {
        this.$Message.error({
          content:"不合法密钥",
          duration:2
        });
        return;
      }
      localStorage.setItem("secret",secret);

      let info=""
      if(this.secret==null)
        info="添加成功";
      else
        info="更改成功";
      this.secret = secret;
      this.pre_secret = "";
      this.modal = false;
      this.$Message.success({
        content:info,
        duration:2
      });
      // 让搜索页面重新获取密钥
      this.$emit("re_get_secret_search");
    },
    check_secret:function()
    {
      let secret = this.pre_secret;
      let original_secret;
      try {
        original_secret = JSON.parse(decode(secret));
      } catch {
        return false;
      }
      
      if(original_secret.word == undefined || original_secret.aes_secret == undefined || original_secret.decrypt_matrix == undefined)
        return false
      return secret;
    },
    delete_ok:function(){
      localStorage.removeItem("secret");
      this.secret = null;
      this.modal_delete = false;
      // 让搜索页面重新获取密钥
      this.$emit("re_get_secret_search");
    }
  }
}
</script>

<style scoped lang="scss">
.user-information
{
  padding:15px 15px 0 15px;
}
.card
{
  border-radius:5px;
  box-shadow:0 2px 2px rgb(200,200,200);
  padding:10px 15px 10px 15px;
  position:relative;
  z-index:0;
  background-color:white;
  font-size:1rem;
  margin-bottom:15px;
}
.introduction
{
  font-size:1.1rem;
  /* margin-bottom:15px; */
  font-weight:bold;
}
.button1
{
  font-size:1rem;
  font-weight:bold;
  // margin-bottom:15px;
  color: #ed4014;
}
.button2
{
  font-size:1rem;
  font-weight:bold;
  // margin-bottom:15px;
  color: #ed4014;
}
// 加载动画
.spin{
    animation: ani-spin 1s linear infinite;
}
@keyframes ani-spin {
    from { transform: rotate(0deg);}
    50%  { transform: rotate(180deg);}
    to   { transform: rotate(360deg);}
}
.tag
{
  font-size:0.9rem;
  height:28px;
  line-height: 26px;
}
.secret
{
  margin-top:4px;
  margin-bottom:6px;
  font-size:0.9rem;
  font-family: "Tahoma";
  max-height:150px;
  overflow-y:hidden;
  overflow-x:hidden;
  font-size:0.8rem;
  word-break:break-all;
  -webkit-user-select: none;
}
.secret-button
{
  display:flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.normal-font
{
  font-size:1rem;
}
.textarea /deep/ .ivu-input
{
  height:150px;
  resize:none;
}
.success
{
  color:#19be6b;
}
.error
{
  color:#ed4014;
}
.margin
{
  width:200px; 
  height:20px;
  margin-top:3px;
  margin-bottom:4px;
}
.one{
  float: left;
  height: 500px;
  width: 1500px;
  display:inline;
}
.two
{
  height: 500px;
  width: 600px;
  float: right;
  display:inline;
}
</style>