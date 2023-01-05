import os
from django.contrib.auth.models import AbstractUser
import pexpect
from django.db import models

# ==== DOCKER COMMANDS
# docker run -v $PWD/vpn-data:/etc/openvpn --rm -it myownvpn easyrsa build-client-full user nopass
# docker run -v $PWD/vpn-data:/etc/openvpn --rm myownvpn ovpn_getclient <USERNAME> > "username".ovpn


class User(AbstractUser):
    config = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Создание config файла пользователя
            # TODO: Измените путь здесь:
            vpn_data_path = '/home/user/vpn-data'
            
            child = pexpect.spawn(
                'docker run -v ' + vpn_data_path + ':/etc/openvpn --rm -it myownvpn easyrsa build-client-full ' + self.username + ' nopass')
            
            child.expect("Type the word 'yes' to continue, or any other input to abort")
            child.sendline('yes')
            
            child.expect('Enter pass phrase for /etc/openvpn/pki/private/ca.key:')
            
            # TODO: Измените CA key здесь:
            child.sendline('cakeypass')
            
            i = child.expect(['Data Base Updated', pexpect.EOF])

            if i == 0:
                print("Certificate Created")
                super().save(*args, **kwargs)
            else:
                print("BAD REQUEST")
                return -1

            # Создание VPN конфигурации с username 
            # TODO: Измените путь здесь::
            output_path = "/home/user/django_openvpn/static/configs/"
            os.system(
                "docker run -v " + vpn_data_path + ":/etc/openvpn --rm myownvpn ovpn_getclient " + self.username + " > " + output_path +
                self.username + ".ovpn")
            print("CONFIG CREATED")
            self.config = '/static/configs/' + self.username + '.ovpn'
            
        super().save(*args, **kwargs)
