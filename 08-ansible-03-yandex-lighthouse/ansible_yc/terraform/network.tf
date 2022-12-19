# Network
resource "yandex_vpc_network" "default-net" {
  name = "default-net"
}

resource "yandex_vpc_subnet" "my-net" {
  name           = "my-net"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.default-net.id
  v4_cidr_blocks = ["10.129.0.0/16"]
}
