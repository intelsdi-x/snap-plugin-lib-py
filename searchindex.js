Search.setIndex({envversion:49,filenames:["index","modules","plugin_authoring/collector","plugin_authoring/index","plugin_authoring/plugin_naming","plugin_authoring/processor","plugin_authoring/publisher","snap_plugin","snap_plugin.v1","snap_plugin.v1.collector","snap_plugin.v1.collector_proxy","snap_plugin.v1.plugin","snap_plugin.v1.plugin_pb2","snap_plugin.v1.plugin_proxy","snap_plugin.v1.processor","snap_plugin.v1.processor_proxy","snap_plugin.v1.publisher","snap_plugin.v1.publisher_proxy"],objects:{"":{snap_plugin:[7,0,0,"-"]},"snap_plugin.v1":{Collector:[8,1,1,""],Processor:[8,1,1,""],Publisher:[8,1,1,""],collector:[9,0,0,"-"],collector_proxy:[10,0,0,"-"],current_timestamp:[8,3,1,""],plugin:[11,0,0,"-"],plugin_pb2:[12,0,0,"-"],plugin_proxy:[13,0,0,"-"],processor:[14,0,0,"-"],processor_proxy:[15,0,0,"-"],publisher:[16,0,0,"-"],publisher_proxy:[17,0,0,"-"]},"snap_plugin.v1.Collector":{collect_metrics:[8,2,1,""],get_metric_types:[8,2,1,""]},"snap_plugin.v1.Processor":{process:[8,2,1,""]},"snap_plugin.v1.Publisher":{publish:[8,2,1,""]},"snap_plugin.v1.collector":{Collector:[9,1,1,""]},"snap_plugin.v1.collector.Collector":{collect_metrics:[9,2,1,""],get_metric_types:[9,2,1,""]},"snap_plugin.v1.collector_proxy":{CollectorProxy:[10,1,1,""]},"snap_plugin.v1.collector_proxy.CollectorProxy":{CollectMetrics:[10,2,1,""],GetMetricTypes:[10,2,1,""]},"snap_plugin.v1.plugin":{EnumEncoder:[11,1,1,""],Meta:[11,1,1,""],Plugin:[11,1,1,""],PluginResponseState:[11,1,1,""],PluginType:[11,1,1,""],RPCType:[11,1,1,""],RoutingStrategy:[11,1,1,""]},"snap_plugin.v1.plugin.EnumEncoder":{"default":[11,2,1,""]},"snap_plugin.v1.plugin.Plugin":{get_config_policy:[11,2,1,""],start_plugin:[11,2,1,""],stop_plugin:[11,2,1,""]},"snap_plugin.v1.plugin.PluginResponseState":{plugin_failure:[11,4,1,""],plugin_success:[11,4,1,""]},"snap_plugin.v1.plugin.PluginType":{collector:[11,4,1,""],processor:[11,4,1,""],publisher:[11,4,1,""]},"snap_plugin.v1.plugin.RPCType":{"native":[11,4,1,""],grpc:[11,4,1,""],json:[11,4,1,""]},"snap_plugin.v1.plugin.RoutingStrategy":{config:[11,4,1,""],lru:[11,4,1,""],sticky:[11,4,1,""]},"snap_plugin.v1.plugin_pb2":{BetaCollectorServicer:[12,1,1,""],BetaCollectorStub:[12,1,1,""],BetaProcessorServicer:[12,1,1,""],BetaProcessorStub:[12,1,1,""],BetaPublisherServicer:[12,1,1,""],BetaPublisherStub:[12,1,1,""],CollectorServicer:[12,1,1,""],CollectorStub:[12,1,1,""],ProcessorServicer:[12,1,1,""],ProcessorStub:[12,1,1,""],PublisherServicer:[12,1,1,""],PublisherStub:[12,1,1,""],add_CollectorServicer_to_server:[12,3,1,""],add_ProcessorServicer_to_server:[12,3,1,""],add_PublisherServicer_to_server:[12,3,1,""],beta_create_Collector_server:[12,3,1,""],beta_create_Collector_stub:[12,3,1,""],beta_create_Processor_server:[12,3,1,""],beta_create_Processor_stub:[12,3,1,""],beta_create_Publisher_server:[12,3,1,""],beta_create_Publisher_stub:[12,3,1,""]},"snap_plugin.v1.plugin_pb2.BetaCollectorServicer":{CollectMetrics:[12,2,1,""],GetConfigPolicy:[12,2,1,""],GetMetricTypes:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.BetaCollectorStub":{CollectMetrics:[12,2,1,""],GetConfigPolicy:[12,2,1,""],GetMetricTypes:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.BetaProcessorServicer":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Process:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.BetaProcessorStub":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Process:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.BetaPublisherServicer":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Publish:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.BetaPublisherStub":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Publish:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.CollectorServicer":{CollectMetrics:[12,2,1,""],GetConfigPolicy:[12,2,1,""],GetMetricTypes:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.ProcessorServicer":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Process:[12,2,1,""]},"snap_plugin.v1.plugin_pb2.PublisherServicer":{GetConfigPolicy:[12,2,1,""],Kill:[12,2,1,""],Ping:[12,2,1,""],Publish:[12,2,1,""]},"snap_plugin.v1.plugin_proxy":{PluginProxy:[13,1,1,""]},"snap_plugin.v1.plugin_proxy.PluginProxy":{GetConfigPolicy:[13,2,1,""],Kill:[13,2,1,""],Ping:[13,2,1,""]},"snap_plugin.v1.processor":{Processor:[14,1,1,""]},"snap_plugin.v1.processor.Processor":{process:[14,2,1,""]},"snap_plugin.v1.processor_proxy":{ProcessorProxy:[15,1,1,""]},"snap_plugin.v1.processor_proxy.ProcessorProxy":{Process:[15,2,1,""]},"snap_plugin.v1.publisher":{Publisher:[16,1,1,""]},"snap_plugin.v1.publisher.Publisher":{publish:[16,2,1,""]},"snap_plugin.v1.publisher_proxy":{PublisherProxy:[17,1,1,""]},"snap_plugin.v1.publisher_proxy.PublisherProxy":{Publish:[17,2,1,""]},snap_plugin:{v1:[8,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:attribute"},terms:{"default":11,"enum":11,"function":[8,14],"import":2,"return":[8,9,11,14,16],"true":11,__init__:[],add:[8,11,13,14,15,16],add_collectorservicer_to_serv:12,add_processorservicer_to_serv:12,add_publisherservicer_to_serv:12,addit:[8,14],allow_nan:11,appli:[8,14],author:[],averag:[8,14],avoid:[8,9],base:[8,9,10,11,12,13,14,15,16,17],below:[0,2,5,6],beta_create_collector_serv:12,beta_create_collector_stub:12,beta_create_processor_serv:12,beta_create_processor_stub:12,beta_create_publisher_serv:12,beta_create_publisher_stub:12,betacollectorservic:12,betacollectorstub:12,betaprocessorservic:12,betaprocessorstub:12,betapublisherservic:12,betapublisherstub:12,call:[8,9,11,14,16],channel:12,check_circular:11,checkout:0,circumst:[8,9],collect:[8,9],collect_metr:[2,8,9],collectmetr:[10,12],collector_metr:2,collector_proxi:[],collectorproxi:10,collectorservic:12,collectorstub:12,config:[8,9,11,14,16],configmap:[8,9],configur:[8,9,11],content:[],context:[8,10,12,13,14,15,17],cover:[2,5,6],current:8,current_timestamp:8,data:[8,9],deamon:[8,9,11,14,16],decis:[2,4],def:2,default_timeout:12,defin:2,describ:11,detail:[0,2,5,6],doc:[8,9],docstr:[8,11,13,14,15],doe:[2,4],done:2,dure:[8,9,14,16],either:[2,4],encod:11,ensure_ascii:11,enumencod:11,error:[8,16],everyth:[],exampl:[8,14,16],execut:[8,9,14],fals:[11,12],few:[8,14],filter:[8,14],find:[0,2,5,6],first:[2,4],follow:[2,4],format:[2,4],framework:0,gener:[],get_config_polici:[2,11],get_metric_typ:[2,8,9],getconfigpolici:[12,13],getconfigpolicyrepli:11,getmetrictyp:[10,12],grpc:11,handshak:[2,4],host:12,how:[],http:0,implement:2,includ:[8,14],indent:11,index:0,initi:[2,4],introduct:0,json:11,jsonencoder:11,just:[8,14],kei:11,kill:[12,13],kwarg:[8,9,11,14,16],later:[2,4],librari:0,like:[8,9],list:[8,9,14,16],load:[8,9,11],lru:11,make:[2,4],max:[8,14],maximum_timeout:12,meta:11,metadata:12,metadata_transform:12,method:[8,9,11,13,14,15,16],metric:[2,8,9,14,16],min:[8,14],modul:[],more:[2,4,8,14,16],must:[8,9,14],nativ:11,need:[2,4],next:2,none:[8,11,12],obj:[8,9,11,14,16],object:[8,11,12,13],occur:[8,16],only:[8,9],option:11,order:2,overriden:[8,9,14],packag:[],page:0,pair:11,paramet:[8,9,14,16],phase:[8,9,14,16],ping:[12,13],plugin_failur:11,plugin_name:[2,4],plugin_pb2:[],plugin_proxi:[],plugin_success:11,pluginproxi:[10,13,15,17],pluginresponsest:11,plugintyp:11,polici:11,pool:12,pool_siz:12,process:[8,12,14,15,16],processor:[],processor_proxi:[],processorproxi:15,processorservic:12,processorstub:12,project:[2,4],protobuf:[],protocol_opt:12,provid:[2,4,8,9],publish:[],publisher_proxi:[],publisherproxi:17,publisherservic:12,publisherstub:12,rand:2,rare:[8,9],repositori:[2,4],request:[8,9,10,12,13,15,17],requir:[8,9,11],routingstrategi:11,rpctype:11,same:[2,4],search:0,see:[8,9],self:2,separ:11,server:12,servic:12,shit:2,should:[8,9],skipkei:11,snap:[0,2,4,5,6,8,9,14,16],snap_plugin:[],snapd:[2,4,8,9,11,14,16],some:2,sort_kei:11,start:2,start_plugin:11,step:2,sticki:11,stop_plugin:11,submodul:[],subpackag:[],successfulli:[8,9],suggest:[2,4,8,9,11],take:[8,14,16],telemetri:0,them:[8,14,16],thi:[0,2,4,8,9,11,14,16],time:8,timeout:12,todo:[8,11,13,14,15,16],type:[2,4,8,9,11,14,16],utf:11,valu:11,version:[8,9,11,14,16],want:2,well:[8,14],what:11,when:[2,4,8,9,11],with_cal:12,workflow:[8,9,14,16],write:[0,2,5,6],you:[0,2,4,5,6],your:[2,4]},titles:["Welcome to the  plugin lib for Python","snap_plugin","Collector","Plugin Authoring","Plugin Naming","Processor","Publisher","snap_plugin package","snap_plugin.v1 package","snap_plugin.v1.collector module","snap_plugin.v1.collector_proxy module","snap_plugin.v1.plugin module","snap_plugin.v1.plugin_pb2 module","snap_plugin.v1.plugin_proxy module","snap_plugin.v1.processor module","snap_plugin.v1.processor_proxy module","snap_plugin.v1.publisher module","snap_plugin.v1.publisher_proxy module"],titleterms:{"class":2,author:3,collector:[2,9],collector_proxi:10,content:[7,8],creat:2,from:2,indice:0,inherit:2,lib:0,modul:[7,8,9,10,11,12,13,14,15,16,17],name:[2,4],packag:[7,8],plugin:[0,2,3,4,11],plugin_pb2:12,plugin_proxi:13,processor:[5,14],processor_proxi:15,publish:[6,16],publisher_proxi:17,python:0,snap_plugin:[1,2,7,8,9,10,11,12,13,14,15,16,17],snaplink:0,submodul:8,subpackag:7,tabl:0,welcom:0}})