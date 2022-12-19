# Заменить на ID своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1geim0buhe7h6mvpbtr"
}

# Заменить на Folder своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1gc0if4fp4krujvnc5u"
}

# Заменить на ID своего образа
# ID можно узнать с помощью команды yc compute image list
variable "centos-7" {
  default = "fd89pepiaem3321iu4n6"
}

variable "instance_cores" {
  default = "2"
}

variable "instance_memory" {
  default = "2"
}
