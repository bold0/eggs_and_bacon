# eggs_and_bacon

#### content.html 
- Conteúdo da msg em HTML.
 
#### subject.txt 
- Subject!
 
#### config.py 
- Configurações!
 
#### /attachments 
- Pasta onde devem ficar os anexos a serem enviados.
 
#### /recipients 
- Mailing list. Podem ser vários arquivos ou um só. O que importa é: um e-mail por linha.

#### /accounts 
Pasta onde ficarão as contas. Cada arquivo refere-se à um provedor diferente.
  - Esquema: o nome do arquivo é a configuração do servidor SMTP.
  ```sh
  <smtp.server.com> <465> <ssl/no_ssl> <starttls/no_starttls>
  ```
  - Conteúdo: Dentro do arquivo devem ficar as contas/senhas no formato: 
  ```sh
  login@server.com\tpassword.
  ```
  - Ou seja, somente o e-mail e senha separados por um TAB(\t).


Divirta-se.
