# ...
STATE_BOUND = "bound"
VOLUME_SOURCES = "volumeSources"
VOLUME_SOURCES_STRING = "volumeSourcesString"
STORAGE_CLASSES = "storageClasses"
SELECTOR_OPERATOR = "selectorOperator"
PERSISTENT_VOLUME = "persistentVolume"

# fields
ACCESS_MODES = "accessModes"
ANNOTATIONS = "annotations"
BASE_TYPE = "baseTypes"
CAPACITY = "capacity"
STORAGE = "storage"
CREATED = "created"
CREATED_TS = "createdTS"
CREATOR_ID = "creatorId"
LABELS = "labels"
LINKS = "links"
REMOVE = "remove"
SELF = "self"
UPDATE = "update"
MOUNT_OPTIONS = "mountOptions"
NAME = "name"
NODE_AFFINITY = "nodeAffinity"
REQUIRED = "required"
NODE_SELECTOR_TERMS = "nodeSelectorTerms"
MATCH_EXPRESSIONS = "matchExpressions"
KEY = "key"
OPERATOR = "operator"
TYPE = "type"
VALUES = "values"
PERSISTENT_VOLUME_RECLAIM_POLICY = "persistentVolumeReclaimPolicy"
STATE = "state"
STATUS = "status"
PHASE = "phase"
STORAGE_CLASS_ID = "storage_class_id"
TRANSITIONING = "transitioning"
TRANSITIONING_MESSAGE = "transitioningMessage"
UUID = "uuid"
VOLUME_MODE = "volumeMode"

# list persistent volumes
CAN_REMOVE = "canRemove"
SOURCE = "source"

# Volume Source Name
AWS_EBS = "aws-ebs"
AZURE_DISK = "azure-disk"
AZURE_FILE = "azure-file"
CSI = "csi"
CEPHFS = "cephfs"
CONFIG_MAP = "config-map"
CINDER = "cinder"
# DOWNWARD_API = "downward_api"
SECRET = "secret"
EMPTY_DIR = "empty-dir"
FC = "fc"
FLEX_VOLUME = "flex-volume"
CSI_VOLUME_LONGHORN = "cs-volume-longhorn"
FLOCKER = "flocker"
GCE_PD = "gce-pd"
# GIT_REPO = "git-repo"
GLUSTERFS = "glusterfs"
HOST_PATH = "host-path"
ISCSI = "iscsi"
LOCAL = "local"
NFS = "nfs"
# PVC = "pvc"
PHOTON = "photon"
PORTWORX = "portworx"
# PROJECTED = "projected"
QUOBYTE = "quobyte"
RBD = "rbd"
SCALEIO = "sacleio"
STORAGEOS = "storageos"
VSPHERE_VOLUME = "vsphere-volume"
CUSTOM_LOG_PATH = "customLogPath"

# Volume Source Title
TITLE_AWS_EBS = "Amazon EBS Disk"
TITLE_AZURE_DISK = "Azure Disk"
TITLE_AZURE_FILE = "Azure Filesystem"
TITLE_CSI = "CSI"
TITLE_CEPHFS = "Ceph Filesystem"
TITLE_CONFIG_MAP = "Config Map Volume"
TITLE_CINDER = "Openstack Cinder Volume"
TITLE_SECRET = "Secret Volume"
TITLE_EMPTY_DIR = "Empty Dir Volume"
TITLE_FC = "Fibre Channel"
TITLE_FLEX_VOLUME = "Flex Volume"
TITLE_CSI_VOLUME_LONGHORN = "Longhorn"
TITLE_FLOCKER = "Flocker"
TITLE_GCE_PD = "Google Persistent Disk"
TITLE_GLUSTERFS = "Gluster Volume"
TITLE_HOST_PATH = "HostPath"
TITLE_ISCSI = "iSCSI Target"
TITLE_LOCAL = "Local"
TITLE_NFS = "NFS Share"
TITLE_PHOTON = "Photon Volume"
TITLE_PORTWORX = "Portworx Volume"
TITLE_QUOBYTE = "Quobyte Volume"
TITLE_RBD = "Ceph RBD"
TITLE_SCALEIO = "ScaleIO Volume"
TITLE_STORAGEOS = "StorageOS"
TITLE_VSPHERE_VOLUME = "VMWare vSphere Volume"

# Key Name
LABEL = "label"
VALUE = "value"

VOLUME_SOURCE = "volumeSource"
TITLE = "title"
FIELD = "field"
COMPONENT = "component"
EPHEMERAL = "ephemeral"
PERSISTENT = "persistent"
SUPPORTED = "supported"
DRIVER = "driver"
CONFIGURATION = "configuration"


# TODO: 해당 json 형식의 data를 converting 하여 대입할 수 있도록 수정.
VOLUME_SOURCE_DICTIONARY = {
    VOLUME_SOURCE: {
        TITLE_AWS_EBS: {
            TITLE: TITLE_AWS_EBS
            , NAME: AWS_EBS
            , FIELD: "awsElasticBlockStore"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "volumeID": {
                    "label": "volume ID"
                    , "type": "label/string"
                    , "placeholder": "e.g. volume1"
                    , "default": ""
                    , "required": True
                }
                , "partition": {
                    "label": "Partition"
                    , "type": "label/int"
                    , "placeholder": "e.g. 1; 0 for entire device"
                    , "default": 0
                    , "required": True
                }
                , "fsType": {
                    "label": "Filesystem Type"
                    , "type": "label/string"
                    , "placeholder": "e.g. ext4"
                    , "default": ""
                    , "required": False
                }
                , "readOnly": {
                    "label": "Read Only"
                    , "type": "radio"
                    , "default": True
                    , "items": [
                        {
                            "label": "Yes"
                            , "value": True
                        }
                        , {
                            "label": "No"
                            , "value": False
                        }
                    ]
                    , "required": True
                }
            }
        }
        , TITLE_AZURE_DISK: {
            TITLE: TITLE_AZURE_DISK
            , NAME: AZURE_DISK
            , FIELD: "azureDisk"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "diskName": {
                    "label": "Disk Name"
                    , "type": "label/string"
                    , "placeholder": "e.g. kubernetes-pvc"
                    , "default": ""
                    , "required": True
                }
                , "diskURI": {
                    "label": "Disk URI"
                    , "type": "label/string"
                    , "placeholder": "e.g. https://example.com/disk"
                    , "default": ""
                    , "required": True
                }
                , "kind": {
                    "label": "Kind"
                    , "type": "radio"
                    , "default": "Shared"
                    , "items": [
                        {
                            "label": "Dedicated"
                            , "value": "Dedicated"
                        }
                        , {
                           "label": "Managed"
                           , "value": "Managed"
                        }
                        , {
                            "label": "Shared"
                            , "value": "Shared"
                        }
                    ]
                    , "required": True
                }
                , "cachingMode": {
                    "label": "Caching Mode"
                    , "type": "radio"
                    , "default": "None"
                    , "items": [
                        {
                            "label": "None"
                            , "value": "None"
                        }
                        , {
                            "label": "Read Only"
                            , "value": "ReadOnly"

                        }
                        , {
                            "label": "Read Write"
                            , "value": "ReadWirte"
                        }
                    ]
                    , "required": True
                }
                , "fsType": {
                    "label": "Filesystem Type"
                    , "type": "label/string"
                    , "placeholder": "e.g. ext4"
                    , "default": ""
                    , "required": False
                }
                , "readOnly": {
                    "label": "Read Only"
                    , "type": "radio"
                    , "default": False
                    , "items": [
                        {
                            "label": "Yes"
                            , "value": True
                        }
                        , {
                            "label": "No"
                            , "value": False
                        }
                    ]
                    , "required": True
                }
            }
        }
        , TITLE_AZURE_FILE: {
            TITLE: TITLE_AZURE_FILE
            , NAME: AZURE_FILE
            , FIELD: "azureFile"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "shareName": {
                    "label": "Share Name"
                    , "type": "label/string"
                    , "placeholder": "e.g. abc"
                    , "default": ""
                    , "required": True
                }
                , "secretName": {
                    "lable": "Secret Name"
                    , "type": "label/string"
                    , "placeholder": "e.g. secret"
                    , "default": ""
                    , "required": True
                }
                , "secretNamespace": {
                    "label": "Secret Namespace"
                    , "type": "label/string"
                    , "placeholder": "e.g. default"
                    , "default": ""
                    , "required": False
                }
                , "readOnly": {
                    "label": "Read Only"
                    , "type": "radio"
                    , "default": True
                    , "items": [
                        {
                            "label": "Yes"
                            , "value": True
                        }
                        , {
                            "label": "No"
                            , "value": False
                        }
                    ]
                    , "required": True
                }
            }
        }
        , TITLE_CSI: {
            TITLE: TITLE_CSI
            , NAME: CSI
            , FIELD: "csi"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_CEPHFS: {
            TITLE: TITLE_CEPHFS
            , NAME: CEPHFS
            , FIELD: "cephfs"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_CONFIG_MAP: {
            TITLE: TITLE_CONFIG_MAP
            , NAME: CONFIG_MAP
            , FIELD: "configMap"
            , COMPONENT: True
            , EPHEMERAL: False
            , PERSISTENT: False
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_CINDER: {
            TITLE: TITLE_CINDER
            , NAME: CINDER
            , FIELD: "cinder"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        # , DOWNWARD_API: {
        #     TITLE: "???"
        #     , NAME: DOWNWARD_API
        #     , FIELD: "downwardAPI"
        #     , COMPONENT: True
        #     , EPHEMERAL: True
        #     , PERSISTENT: False
        #     , SUPPORTED: False
        #     , DRIVER: ''
        # }
        , TITLE_SECRET: {
            TITLE: TITLE_SECRET
            , NAME: SECRET
            , FIELD: "secret"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: False
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_EMPTY_DIR: {
            TITLE: TITLE_EMPTY_DIR
            , NAME: EMPTY_DIR
            , FIELD: "emptyDir"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: False
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_FC: {
            TITLE: TITLE_FC
            , NAME: FC
            , FIELD: "fc"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_FLEX_VOLUME: {
            TITLE: TITLE_FLEX_VOLUME
            , NAME: FLEX_VOLUME
            , FIELD: "flexVolume"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_CSI_VOLUME_LONGHORN: {
            TITLE: TITLE_CSI_VOLUME_LONGHORN
            , NAME: CSI_VOLUME_LONGHORN
            , FIELD: "csi"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: 'driver.longhorn.io'
            , CONFIGURATION: {
                "driver": {
                    "label": "Driver"
                    , "type": "label/fix"
                    , "placeholder": ""
                    , "default": "driver.longhorn.io"
                    , "required": True
                }
                , "volumeAttributes": {
                    "label": "Options"
                    , "type": "map/addable"
                    , "default": {
                        "size": "2Gi"
                        , "numberOfReplicas": "3"
                        , "staleReplicaTimeout": "20"
                        , "fromBackup": ""
                    }
                    , "required": True
                }
                , "fsType": {
                    "label": "Filesystem Type"
                    , "type": "label/string"
                    , "placeholder": "e.g. ext4"
                    , "default": ""
                    , "required": False
                }
                , "readOnly": {
                    "label": "Read Only"
                    , "type": "radio"
                    , "default": True
                    , "items": [
                        {
                            "label": "Yes"
                            , "value": True
                        }
                        , {
                            "label": "No"
                            , "value": False
                        }
                    ]
                    , "required": True
                }
                , "volumeHandle": {
                    "label": "Volume Handle"
                    , "type": "label/string"
                    , "placeholder": "e.g. pvc-xxxx"
                    , "default": ""
                    , "required": True
                }
            }
        }
        , TITLE_FLOCKER: {
            TITLE: TITLE_FLOCKER
            , NAME: FLOCKER
            , FIELD: "flocker"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_GCE_PD: {
            TITLE: TITLE_GCE_PD
            , NAME: GCE_PD
            , FIELD: "gcePersistentDisk"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "pdName": {
                    "label": "Persistent Disk Name"
                    , "type": "label/string"
                    , "placeholder": "e.g. abc"
                    , "default": ""
                    , "required": True
                }
                , "partition": {
                    "label": "Partition"
                    , "type": "label/int"
                    , "placeholder": "e.g. 1; 0 for entire device"
                    , "default": 0
                    , "required": True
                }
                , "fsType": {
                    "label": "Filesystem Type"
                    , "type": "label/string"
                    , "placeholder": "e.g. ext4"
                    , "default": ""
                    , "required": False
                }
                , "readOnly": {
                    "label": "Read Only"
                    , "type": "radio"
                    , "default": True
                    , "items": [
                        {
                            "label": "Yes"
                            , "value": True
                        }
                        , {
                            "label": "No"
                            , "value": False
                        }
                    ]
                    , "required": True
                }
            }
        }
        # , GIT_REPO: {
        #     TITLE: "???"
        #     , NAME: GIT_REPO
        #     , FIELD: "gitRepo"
        #     , COMPONENT: True
        #     , EPHEMERAL: True
        #     , PERSISTENT: False
        #     , SUPPORTED: False
        #     , DRIVER: ''
        # }
        , TITLE_GLUSTERFS: {
            TITLE: TITLE_GLUSTERFS
            , NAME: GLUSTERFS
            , FIELD: "glusterfs"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_HOST_PATH: {
            TITLE: TITLE_HOST_PATH
            , NAME: HOST_PATH
            , FIELD: "hostPath"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "path": {
                    "label": "Path on the Node"
                    , "type": "label/string"
                    , "placeholder": "e.g. /data"
                    , "default": ""
                    , "required": True
                }
                , "kind": {
                    "label": "The Path on the Node must be"
                    , "type": "select"
                    , "default": "Any"
                    , "items": [
                        {
                            "label": "Anything: do no check the target path"
                            , "value": "Any"
                        }
                        , {
                            "label": "A directory, or create if it does not exist"
                            , "value": "DirectoryOrCreate"
                        }
                        , {
                            "label": "A file, or create if it does not exists"
                            , "value": "FileOrCreate"
                        }
                        , {
                            "label": "An existing directory"
                            , "value": "Directory"
                        }
                        , {
                            "label": "An existing file"
                            , "value": "File"
                        }
                        , {
                            "label": "An existing socket"
                            , "value": "Socket"
                        }
                        , {
                            "label": "An existing character device"
                            , "value": "CharDevice"
                        }
                        , {
                            "label": "An existing block device"
                            , "value": "BlockDevice"
                        }
                    ]
                    , "required": True
                }
            }
        }
        , TITLE_ISCSI: {
            TITLE: TITLE_ISCSI
            , NAME: ISCSI
            , FIELD: "iscsi"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_LOCAL: {
            TITLE: TITLE_LOCAL
            , NAME: LOCAL
            , FIELD: "local"
            , COMPONENT: True
            , EPHEMERAL: False
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "path": {
                    "label": "Path"
                    , "type": "label/string"
                    , "placeholder": "e.g. /mnt/disks/ssd1"
                    , "default": ""
                    , "required": True
                }
            }
        }
        , TITLE_NFS: {
            TITLE: TITLE_NFS
            , NAME: NFS
            , FIELD: "nfs"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "path": {
                    "label": "Path"
                    , "type": "label/string"
                    , "placeholder": "e.g. /var"
                    , "default": ""
                    , "required": True
                }
                , "server": {
                    "label": "Server"
                    , "type": "label/string"
                    , "placeholder": "e.g. 10.244.1.4"
                    , "default": ""
                    , "required": True
                }
            }
        }
        # , PVC: {
        #     TITLE: "???"
        #     , NAME: PVC
        #     , FIELD: "persistentVolumeClaim"
        #     , COMPONENT: True
        #     , EPHEMERAL: True
        #     , PERSISTENT: False
        #     , SUPPORTED: False
        #     , DRIVER: ''
        # }
        , TITLE_PHOTON: {
            TITLE: TITLE_PHOTON
            , NAME: PHOTON
            , FIELD: "photonPersistentDisk"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_PORTWORX: {
            TITLE: TITLE_PORTWORX
            , NAME: PORTWORX
            , FIELD: "portworxVolume"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        # , PROJECTED: {
        #     TITLE: "???"
        #     , NAME: PROJECTED
        #     , FIELD: "projected"
        #     , COMPONENT: True
        #     , EPHEMERAL: True
        #     , PERSISTENT: False
        #     , SUPPORTED: False
        #     , DRIVER: ''
        # }
        , TITLE_QUOBYTE: {
            TITLE: TITLE_QUOBYTE
            , NAME: QUOBYTE
            , FIELD: "quobyte"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_RBD: {
            TITLE: TITLE_RBD
            , NAME: RBD
            , FIELD: "rbd"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_SCALEIO: {
            TITLE: TITLE_SCALEIO
            , NAME: SCALEIO
            , FIELD: "scaleIO"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_STORAGEOS: {
            TITLE: TITLE_STORAGEOS
            , NAME: STORAGEOS
            , FIELD: "storageos"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: False
            , DRIVER: ''
        }
        , TITLE_VSPHERE_VOLUME: {
            TITLE: TITLE_VSPHERE_VOLUME
            , NAME: VSPHERE_VOLUME
            , FIELD: "vsphereVolume"
            , COMPONENT: True
            , EPHEMERAL: True
            , PERSISTENT: True
            , SUPPORTED: True
            , DRIVER: ''
            , CONFIGURATION: {
                "volumePath": {
                    "label": "Volume Path"
                    , "type": "label/string"
                    , "placeholder": "e.g. /"
                    , "default": ""
                    , "required": True
                }
                , "storagePolicyName": {
                    "label": "Storage Policy Name"
                    , "type": "label/string"
                    , "placeholder": "e.g. sp"
                    , "default": ""
                    , "required": False
                }
                , "storagePolicyID": {
                    "label": "Storage Policy ID"
                    , "type": "label/string"
                    , "placeholder": "e.g. sp1"
                    , "default": ""
                    , "required": False
                }
                , "fsType": {
                    "label": "Filesystem Type"
                    , "type": "label/string"
                    , "placeholder": "e.g. ext4"
                    , "default": ""
                    , "required": False
                }
            }
        }
        , CUSTOM_LOG_PATH: {
            "mountPath": {
                "label": "Log Path"
                , "placeholder": "e.g. /var/www"
                , "helpText": "Your log path inside the container"
            }
            , "logFormat": {
                "label": "Log Format"
                , "useCustomRegex": "Use a custom Fluentd regex"
                , "useExistingLogFormat": "Use an existing log format"
                , "helpText": 'You can test your regex <a href="http://fluentular.herokuapp.com/" '
                              'target="_blank">here</a> '
            }
        }
    }
}

VOLUME_NODE_SELECTOR_OPERATOR = [
    {
        LABEL: "is set"
        , VALUE: "Exists"
    }
    , {
        LABEL: "is not set"
        , VALUE: "DoesNotExist"
    }
    , {
        LABEL: "in list"
        , VALUE: "In"
    }
    , {
        LABEL: "not in list"
        , VALUE: "NotIn"
    }
    ,
]

FORM_ACCESS_MODES = {
    "label": "Access Modes"
    , "mode": [
        {
            "id": "accessRWO"
            , LABEL: "Single Node Read-Write"
            , VALUE: "ReadWriteOnce"
        }
        , {
            "id": "accessROX"
            , LABEL: "Many Nodes Read-Only"
            , VALUE: "ReadOnlyMany"
        }
        , {
            "id": "accessRWX"
            , LABEL: "Many Nodes Read-Write"
            , VALUE: "ReadWriteMany"
        }
    ]
}


# amazon EBS Disk Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce",
#       "ReadOnlyMany",
#       "ReadWriteMany"
#    ],
#    "name":"amazon",
#    "azureDisk":null,
#    "azureFile":null,
#    "gcePersistentDisk":null,
#    "hostPath":null,
#    "awsElasticBlockStore":{
#       "partition":0,
#       "readOnly":false,
#       "type":"awselasticblockstorevolumesource",
#       "volumeID":"volume1",
#       "fsType":null
#    },
#    "mountOptions":[
#       "value1",
#       "value2"
#    ],
#    "nodeAffinity":{
#       "required":{
#          "nodeSelectorTerms":[
#             {
#                "matchExpressions":[
#                   {
#                      "key":"rule1",
#                      "operator":"In",
#                      "values":[
#                         "rule1"
#                      ]
#                   }
#                ]
#             },
#             {
#                "matchExpressions":[
#                   {
#                      "key":"rule2",
#                      "operator":"In",
#                      "values":[
#                         "rule2"
#                      ]
#                   },
#                   {
#                      "key":"rule2_2",
#                      "operator":"DoesNotExist"
#                   }
#                ]
#             }
#          ]
#       }
#    },
#    "capacity":{
#       "storage":"1Gi"
#    }
# }

# Azure Disk
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"azure",
#    "azureDisk":{
#       "type":"azurediskvolumesource",
#       "readOnly":false,
#       "cachingMode":"None",
#       "kind":"Shared",
#       "diskName":"test",
#       "diskURI":"https://test.com/test"
#    },
#    "capacity":{
#       "storage":"10Gi"
#    }
# }

# Azure Filesystem Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"azure-filesystem2",
#    "azureFile":{
#       "readOnly":false,
#       "type":"azurefilepersistentvolumesource",
#       "shareName":"aaa",
#       "secretName":"secret",
#       "secretNamespace":"dddef"
#    },
#    "capacity":{
#       "storage":"10Gi"
#    }
# }

# Google Persistent Disk Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"google-persistent-disk",
#    "azureFile":null,
#    "gcePersistentDisk":{
#       "partition":0,
#       "readOnly":false,
#       "type":"gcepersistentdiskvolumesource",
#       "pdName":"test",
#       "fsType":"ext4"
#    },
#    "capacity":{
#       "storage":"10Gi"
#    }
# }

# Longhorn Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"longhorn",
#    "awsElasticBlockStore":null,
#    "local":null,
#    "csi":{
#       "readOnly":false,
#       "type":"csipersistentvolumesource",
#       "driver":"driver.longhorn.io",
#       "volumeAttributes":{
#          "size":"2Gi",
#          "numberOfReplicas":"3",
#          "staleReplicaTimeout":"20"
#       },
#       "volumeHandle":"pvc-xxxx",
#       "fsType":"ext4"
#    },
#    "capacity":{
#       "storage":"1Gi"
#    }
# }

# NFS Volume Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"nfs",
#    "nfs":{
#       "readOnly":false,
#       "type":"nfsvolumesource",
#       "path":"/var",
#       "server":"10.244.1.4"
#    },
#    "capacity":{
#       "storage":"10Gi"
#    }
# }

# VMWare vSphere Volume Create Sample
# {
#    "type":"persistentVolume",
#    "accessModes":[
#       "ReadWriteOnce"
#    ],
#    "name":"vmtest",
#    "vsphereVolume":{
#       "type":"vspherevirtualdiskvolumesource",
#       "volumePath":"/",
#       "storagePolicyName":"sp",
#       "storagePolicyID":"sp1",
#       "fsType":"ext4"
#    },
#    "capacity":{
#       "storage":"10Gi"
#    }
# }
