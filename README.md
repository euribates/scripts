# scripts

Scripts de utilidad


## SAS

**SAS Viya** es una plataforma de anælisis, gestión de datos e
inteligencia artificical desarrollado por [SAS Institute]().


TODO:

- Usar el cliente SAS para verificar que el usuario que queremos crear
  existe en sas-viya. De paso, obtener el nombre y apellidos para
  incluirlo en el fichero `/etc/passwd`.

- Poder dar de alta a varias usuarios con un solo grupo


### Algunas operaciones que podemos hacer con el cliente SAS

Estas operaciones hacen uso de un _plugin_ llamado `identities`.

#### Cómo listar los grupos de usuarios

```
$ sudo sas-viya identities list-groups
```

#### Cómo ver los detalles de un grupo

```
$ sudo sas-viya identities show-group --id <id. del grupo>
```

#### Cómo listar los usuarios

```
$ sudo sas-viya identities list-users
```

#### Cómo ver los detalles de un usuario

```
