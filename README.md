<!--
 * @Date: 2022-01-11 18:08:25
 * @LastEditors: recar
 * @LastEditTime: 2022-03-28 18:26:28
-->
# mullet
被动代理扫描器 梭鱼


代理模块  
url去重模块  
任务分发模块 多生产者多消费者模块 多队列形式  
指纹识别模块  
poc通用模块  
通用检测模块  
漏洞报告模块  
日志模块 日志要酷炫  
参数控制模块  

一个流程:  
指纹识别->分析出是啥指纹后增加poc任务
敏感目录备份文件等扫描
上面一个url就可以添加出来任务了

然后代理访问开始后或者后续流量有url的就交给url识别  
安装证书 代理开启后访问 http://mitm.it/  

通用检测插件还有哪些要做的 列个计划去做  
sql注入    
xss检测    
命令注入  

可以参考 https://github.com/chaitin/xray  

通用漏洞靶场 https://github.com/Yavuzlar/VulnLab  
