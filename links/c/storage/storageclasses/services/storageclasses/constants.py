# ...
STATE_STRING = "state"
PROVISIONER = "provisioner"
PROVISIONER_STRING = "provisionerString"
DEFAULT_STATE = "active"

# field name
NAME = "name"
DESCRIPTION = "description"
MOUNT_OPTIONS = "mountOptions"
RECLAIM_POLICY = "reclaimPolicy"
VOLUME_BINDING_MODE = "volumeBindingMode"
ALLOW_VOLUME_EXPANSION = "allowVolumeExpansion"

# Storage Class Name
AWS_EBS = "aws-ebs"
AZURE_DISK = "azure-disk"
AZURE_FILE = "azure-file"
LOCAL_STORAGE = "local_storage"
CINDER = "cinder"
GCE_PD = "gce-pd"
GLUSTERFS = "glusterfs"
# LOCAL = "local"
LONGHORN = "longhorn"
PORTWORX_VOLUME = "portworx-volume"
QUOBYTE = "quobyte"
RBD = "rbd"
SCALEIO = "scaleio"
STORAGEOS = "storageos"
VSPHERE_VOLUME = "vsphere-volume"

# Storage Class Title
TITLE_AWS_EBS = "Amazon EBS Disk"
TITLE_AZURE_DISK = "Azure Disk"
TITLE_AZURE_FILE = "Azure Filesystem"
TITLE_LOCAL_STORAGE = "Local Storage"
TITLE_CINDER = "Openstack Cinder Volume"
TITLE_GCE_PD = "Google Persistent Disk"
TITLE_GLUSTERFS = "Gluster Volume"
# TITLE_LOCAL = "Local"
TITLE_LONGHORN = "Longhorn"
TITLE_PORTWORX = "Portworx Volume"
TITLE_QUOBYTE = "Quobyte Volume"
TITLE_RBD = "Ceph RBD"
TITLE_SCALEIO = "ScaleIO Volume"
TITLE_STORAGEOS = "StorageOS"
TITLE_VSPHERE_VOLUME = "VMWare vSphere Volume"

# Key Name
STORAGE_CLASS = "storageClass"
STORAGE_CLASS_STRING = "storageClassString"
ID = "id"
LABEL = "label"
DETAIL = "detail"
TYPE = "type"
VALUE = "value"
FIELD = "field"
TITLE = "title"
DEFAULT = "default"
CONDITION = "condition"
ITEMS = "items"
ACTION = "action"
ACTION_PARAMETER = "actionParameter"
COMPONENT = "component"
SUPPORTED = "supported"
PLACEHOLDER = "placeholder"
CONFIGURATION = "configuration"
REQUIRED = "required"
RELATED = "related"

STORAGE_CLASS_DICTIONARY = {
    STORAGE_CLASS: {
        AWS_EBS: {
            TITLE: TITLE_AWS_EBS
            , NAME: AWS_EBS
            , PROVISIONER: "kubernetes.io/aws-ebs"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.type": {
                    LABEL: "Volume Type"
                    , TYPE: "radio"
                    , ID: "parameters.type"
                    , DEFAULT: "gp2"
                    , CONDITION: None
                    , RELATED: [
                        {
                            # trigger의 값은, jquery의 event function 값.
                            "trigger": "change"
                            , "attribute": "value"
                            , VALUE: "io1"
                            , "targetId": "parameters.iopsPerGB"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , ITEMS: [
                        {
                            LABEL: "GP2 - General Purpose SSD"
                            , VALUE: "gp2"
                        }
                        , {
                            LABEL: "IO1 - Provisioned IOPS SSD"
                            , VALUE: "io1"
                        }
                        , {
                            LABEL: "ST1 - Throughput-Optimized HDD"
                            , VALUE: "st1"
                        }
                        , {
                            LABEL: "SC1 - Cold-Storage HDD"
                            , VALUE: "sc1"
                        }
                    ]
                    , REQUIRED: True
                }
                , "parameters.iopsPerGB": {
                    LABEL: "Provisioned IOPS"
                    , TYPE: "label/int"
                    , ID: "parameters.iopsPerGB"
                    , PLACEHOLDER: "per second, per GB"
                    , DEFAULT: ""
                    , CONDITION: [
                        {
                            ID: "parameters.type"
                            , VALUE: "io1"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: False
                }
                , "none.availabilityZone": {
                    LABEL: "Availability Zone"
                    , TYPE: "radio"
                    , ID: "none.availabilityZone"
                    , DEFAULT: "automatic"
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Automatic: Zones the cluster has a node in"
                            , VALUE: "automatic"
                        }
                        , {
                            LABEL: "Manual: Choose specific zones"
                            , VALUE: "manual"
                        }
                    ]
                    , RELATED: [
                        {
                            # trigger의 값은, jquery의 event function 값.
                            "trigger": "change"
                            , "attribute": "value"
                            , VALUE: "manual"
                            , "targetId": "parameters.zones"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , REQUIRED: False
                }
                , "parameters.zones": {
                    LABEL: ""
                    , TYPE: "label/string"
                    , ID: "parameters.zones"
                    , PLACEHOLDER: "us-east-1d, us-east-1c"
                    , DEFAULT: ""
                    , CONDITION: [
                        {
                            ID: "none.availabilityZone"
                            , VALUE: "manual"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.encrypted": {
                    LABEL: "Encryption"
                    , TYPE: "radio"
                    , ID: "parameters.encrypted"
                    , DEFAULT: False
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Enabled"
                            , VALUE: True
                        }
                        , {
                            LABEL: "Disabled"
                            , VALUE: False
                        }
                    ]
                    , RELATED: [
                        {
                            # trigger의 값은, jquery의 event function 값.
                            "trigger": "change"
                            , "attribute": "value"
                            , VALUE: True
                            , "targetId": "none.kmsKeyIdForEncryption"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , REQUIRED: True
                }
                , "none.kmsKeyIdForEncryption": {
                    LABEL: "KMS Key Id for Encryption"
                    , TYPE: "radio"
                    , ID: "none.kmsKeyIdForEncryption"
                    , DEFAULT: "automatic"
                    , CONDITION: [
                        {
                            ID: "parameters.encrypted"
                            , VALUE: True
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , ITEMS: [
                        {
                            LABEL: "Automatic: Generate a key"
                            , VALUE: "automatic"
                        }
                        , {
                            LABEL: "Manual: Use a specific key (full ARN)"
                            , VALUE: "manual"
                        }
                    ]
                    , RELATED: [
                        {
                            # trigger의 값은, jquery의 event function 값.
                            "trigger": "change"
                            , "attribute": "value"
                            , VALUE: "manual"
                            , "targetId": "parameters.kmsKeyId"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , REQUIRED: False
                }
                , "parameters.kmsKeyId": {
                    LABEL: ""
                    , TYPE: "label/string"
                    , ID: "parameters.kmsKeyId"
                    , PLACEHOLDER: ""
                    , DEFAULT: ""
                    , CONDITION: [
                        {
                            ID: "parameters.encrypted"
                            , VALUE: True
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                        , {
                            ID: "none.kmsKeyIdForEncryption"
                            , VALUE: "manual"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.fsType": {
                    LABEL: "Filesystem Type"
                    , TYPE: "label/string"
                    , ID: "parameters.fsType"
                    , PLACEHOLDER: "e.g. ext4"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
            }
        }
        , GCE_PD: {
            TITLE: TITLE_GCE_PD
            , NAME: GCE_PD
            , PROVISIONER: "kubernetes.io/gce-pd"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.type": {
                    LABEL: "Volume Type"
                    , TYPE: "radio"
                    , ID: "parameters.type"
                    , DEFAULT: "pd-standard"
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Standard"
                            , VALUE: "pd-standard"
                        }
                        , {
                            LABEL: "SSD"
                            , VALUE: "pd-ssd"
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: True
                }
                , "none.availabilityZone": {
                    LABEL: "Availability Zone"
                    , TYPE: "radio"
                    , ID: "none.availabilityZone"
                    , DEFAULT: "automatic"
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Automatic: Zones the cluster has a node in"
                            , VALUE: "automatic"
                        }
                        , {
                            LABEL: "Manual: Choose specific zones"
                            , VALUE: "manual"
                        }
                    ]
                    , RELATED: [
                        {
                            # trigger의 값은, jquery의 event function 값.
                            "trigger": "change"
                            , "attribute": "value"
                            , VALUE: "manual"
                            , "targetId": "parameters.zones"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                        }
                        }
                    ]
                    , REQUIRED: False
                }
                , "parameters.zones": {
                    LABEL: ""
                    , TYPE: "label/string"
                    , ID: "parameters.zones"
                    , PLACEHOLDER: "us-central1-a, us-central1-b"
                    , DEFAULT: ""
                    , CONDITION: [
                        {
                            ID: "none.availabilityZone"
                            , VALUE: "manual"
                            , ACTION: "style.visibility"
                            , ACTION_PARAMETER: {
                                "OK": "visible"
                                , "NG": "hidden"
                            }
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.fsType": {
                    LABEL: "Filesystem Type"
                    , TYPE: "label/string"
                    , ID: "parameters.fsType"
                    , PLACEHOLDER: "e.g. ext4"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.replication-type": {
                    LABEL: "Replication Type"
                    , TYPE: "radio"
                    , ID: "parameters.replication-type"
                    , DEFAULT: ""
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Zonal"
                            , VALUE: ""
                        }
                        , {
                            LABEL: "Regional"
                            , VALUE: "regional-pd"
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: False
                }
            }
        }
        , GLUSTERFS: {
            TITLE: TITLE_GLUSTERFS
            , NAME: GLUSTERFS
            , PROVISIONER: "kubernetes.io/glusterfs"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , CINDER: {
            TITLE: TITLE_CINDER
            , NAME: CINDER
            , PROVISIONER: "kubernetes.io/cinder"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , VSPHERE_VOLUME: {
            TITLE: TITLE_VSPHERE_VOLUME
            , NAME: VSPHERE_VOLUME
            , PROVISIONER: "kubernetes.io/vsphere-volume"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.diskformat": {
                    LABEL: "Disk Foramt"
                    , TYPE: "radio"
                    , ID: "parameters.diskformat"
                    , DEFAULT: "thin"
                    , CONDITION: None
                    , RELATED: None
                    , ITEMS: [
                        {
                            LABEL: "Thin"
                            , VALUE: "thin"
                        }
                        , {
                            LABEL: "Zeroed Thick"
                            , VALUE: "zeroedthick"
                        }
                        , {
                            LABEL: "Eager Zeroed Thick"
                            , VALUE: "eagerzeroedthick"
                        }
                    ]
                    , REQUIRED: True
                }
                , "parameters.storagePolicyName": {
                    LABEL: "Storage Policy Name"
                    , TYPE: "label/string"
                    , ID: "parameters.storagePolicyName"
                    , PLACEHOLDER: "e.g. gold"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.datastore": {
                    LABEL: "Datastore"
                    , TYPE: "label/string"
                    , ID: "parameters.datastore"
                    , PLACEHOLDER: "e.g. VSANDatastore"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.hostFailuresToTolerate": {
                    LABEL: "Host Failures To Tolerate"
                    , TYPE: "label/string"
                    , ID: "parameters.hostFailuresToTolerate"
                    , PLACEHOLDER: "e.g. 2"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.cachereservation": {
                    LABEL: "Cache Reservation"
                    , TYPE: "label/string"
                    , ID: "parameters.cachereservation"
                    , PLACEHOLDER: "e.g. 20"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.fstype": {
                    LABEL: "Filesystem Type"
                    , TYPE: "label/string"
                    , ID: "parameters.fstype"
                    , PLACEHOLDER: "e.g. ext3"
                    , DEFAULT: ""
                    , CONDITION: ""
                    , RELATED: None
                    , REQUIRED: False
                }
            }
        }
        , RBD: {
            TITLE: TITLE_RBD
            , NAME: RBD
            , PROVISIONER: "kubernetes.io/rbd"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , QUOBYTE: {
            TITLE: TITLE_QUOBYTE
            , NAME: QUOBYTE
            , PROVISIONER: "kubernetes.io/quobyte"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , AZURE_DISK: {
            TITLE: TITLE_AZURE_DISK
            , NAME: AZURE_DISK
            , PROVISIONER: "kubernetes.io/azure-disk"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.storageaccounttype": {
                    LABEL: "Storage Account Type"
                    , TYPE: "label/string"
                    , ID: "parameters.storageaccounttype"
                    , PLACEHOLDER: "e.g. Standard_LRS"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.kind": {
                    LABEL: "Kind"
                    , TYPE: "select"
                    , ID: "parameters.kind"
                    , DEFAULT: "shared"
                    , CONDITION: None
                    , ITEMS: [
                        {
                            LABEL: "Shared (unmanaged disk)"
                            , VALUE: "shared"
                        }
                        , {
                            LABEL: "Dedicated (unmanaged disk)"
                            , VALUE: "dedicated"
                        }
                        , {
                            LABEL: "Managed"
                            , VALUE: "managed"
                        }
                    ]
                    , RELATED: None
                    , REQUIRED: True
                }
            }
        }
        , AZURE_FILE: {
            TITLE: TITLE_AZURE_FILE
            , NAME: AZURE_FILE
            , PROVISIONER: "kubernetes.io/azure_file"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.skuName": {
                    LABEL: "Sku Name"
                    , TYPE: "label/string"
                    , ID: "parameters.skuName"
                    , PLACEHOLDER: "e.g. Standard_LRS"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.location": {
                    LABEL: "Location"
                    , TYPE: "label/string"
                    , ID: "parameters.location"
                    , PLACEHOLDER: "e.g. eastus"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
                , "parameters.storageAccount": {
                    LABEL: "Storage Account"
                    , TYPE: "label/string"
                    , ID: "parameters.storageAccount"
                    , PLACEHOLDER: "e.g. azure_storage_account_name"
                    , DEFAULT: ""
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
            }
        }
        , PORTWORX_VOLUME: {
            TITLE: TITLE_PORTWORX
            , NAME: PORTWORX_VOLUME
            , PROVISIONER: "kubernetes.io/portworx-volume"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , SCALEIO: {
            TITLE: TITLE_SCALEIO
            , NAME: SCALEIO
            , PROVISIONER: "kubernetes.io/scaleio"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , STORAGEOS: {
            TITLE: TITLE_STORAGEOS
            , NAME: STORAGEOS
            , PROVISIONER: "kubernetes.io/storageos"
            , COMPONENT: True
            , SUPPORTED: False
        }
        , LONGHORN: {
            TITLE: TITLE_LONGHORN
            , NAME: LONGHORN
            , PROVISIONER: "driver.longhorn.io"
            , COMPONENT: True
            , SUPPORTED: True
            , CONFIGURATION: {
                "parameters.options": {
                    LABEL: ""
                    , TYPE: "map/addable"
                    , ID: "parameters.options.none"
                    , DEFAULT: {
                        "numberOfReplicas": "3"
                        , "staleReplicaTimeout": "2880"
                        , "fromBackup": ""
                        , "diskSelector": ""
                        , "nodeSelector": ""
                        , "recurringJobs": ""
                    }
                    , CONDITION: None
                    , RELATED: None
                    , REQUIRED: False
                }
            }
        }
        , LOCAL_STORAGE: {
            TITLE: TITLE_LOCAL_STORAGE
            , NAME: LOCAL_STORAGE
            , PROVISIONER: "kubernetes.io/no-provisioner"
            , COMPONENT: True
            , SUPPORTED: False
        }
    }
}

CRU_STORAGE_CLASS = {
    NAME: {
        LABEL: "Name"
        , PLACEHOLDER: "e.g. storage"
    }
    , DESCRIPTION: {
        LABEL: "Description"
        , PLACEHOLDER: "e.g. AWS EBS Storage"
    }
    , TITLE: {
        "new": "Add Storage Class"
        , "edit": "Edit Storage Class: {name}"
        , "view": "Storage Class: {name}"
    }
    , "parameters": {
        LABEL: "Parameters"
        , DETAIL: "Configure the provider-specific parameters for the storage class"
    }
    , "customize": {
        LABEL: "Customize"
        , DETAIL: "Customize advanced options"
    }
    , MOUNT_OPTIONS: {
        LABEL: "Mount Options"
        , FIELD: MOUNT_OPTIONS
        , "addActionLabel": "Add Option"
        , PLACEHOLDER: "Value"
        , "noData": "No Mount Options"
    }
    , PROVISIONER: {
        LABEL: "Provisioner"
    }
    , RECLAIM_POLICY: {
        LABEL: "Reclaim Policy"
        , FIELD: RECLAIM_POLICY
        , TYPE: "radio"
        , ITEMS: [
            {
                LABEL: "Delete volumes and underlying device when volume claim is deleted"
                , VALUE: "Delete"
            }
            , {
                LABEL: "Retain the volume for manual cleanup"
                , VALUE: "Retail"
            }
            , {
                LABEL: "Recycle: Empty the contents and then preserve the volume for future workloads"
                , VALUE: "Recycle"
            }
        ]
    }
    , VOLUME_BINDING_MODE: {
        LABEL: "Volume Binding Mode"
        , FIELD: VOLUME_BINDING_MODE
        , TYPE: "radio"
        , ITEMS: [
            {
                LABEL: "Bind and provision a persistent volume once the PersistentVolumeClaim is created"
                , VALUE: "immediate"
            }
            , {
                LABEL: "Bind and provision a persistent volume once a Pod using the PersistentVolumeClaim is created"
                , VALUE: "waitForFirstConsumer"
            }
        ]
    }
}

# Amazon EBS Disk Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/aws-ebs",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":"first",
#    "parameters":{
#       "type":"gp2",               # required = true
#       "encrypted":"false",        # required = true
#       "fsType":"ext4"             # required = false
#    }
# }

# Amazon EBS Disk Create Sample 2
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/aws-ebs",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":"second",
#    "parameters":{
#       "type":"io1",            # required = true
#       "zones":"abcd,efgh",     # required = false
#       "iopsPerGB":"1541",      # required = false
#       "encrypted":"false",     # required = true
#       "fsType":"ext4"          # required = false
#    }
# }

# Amazon EBS Disk Create Sample 3
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/aws-ebs",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":"third",
#    "parameters":{
#       "type":"io1",               # required = true
#       "zones":"abc",              # required = false   # 조건 : Avility Zone이 Manual인 경우.
#       "iopsPerGB":"111",          # required = false   # 조건 : type이 io1인 경우.
#       "encrypted":"true",         # required = true
#       "kmsKeyId":"dkenfkejf",     # required = false   # 조건 : Ecryption이 true, KMS Key ID for Encryption이 Manual인 경우.
#       "fsType":"ext4"             # required = false
#    }
# }

# Azure Disk Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/azure-disk",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":"first",
#    "parameters":{
#       "storageaccounttype":"abcdef",  # required = false
#       "kind":"managed"                # required = true
#    }
# }

# Azure File Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/azure-file",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":"first",
#    "parameters":{
#       "skuName":"abc",            # required = false
#       "location":"def",           # required = false
#       "storageAccount":"ghi"      # required = false
#    }
# }

# Google Persistent Disk Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/gce-pd",
#    "reclaimPolicy":"Retain",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":null,
#    "parameters":{
#       "type":"pd-ssd",                    # required = true
#       "fsType":"ext4",                    # required = false
#       "replication-type":"regional-pd",   # required = true
#       "zones":"abc, def"                  # required = false
#    }
# }

# Longhorn Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"driver.longhorn.io",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":true,
#    "volumeBindingMode":"Immediate",
#    "name":"third",
#    "parameters":{                         # required = false
#       "numberOfReplicas":"3",
#       "staleReplicaTimeout":"2880"
#    }
# }

# VMWare vSphere Volume Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"kubernetes.io/vsphere-volume",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":null,
#    "parameters":{
#       "diskformat":"eagerzeroedthick",    # required = false
#       "storagePolicyName":"aa",           # required = false
#       "datastore":"bb",                   # required = false
#       "hostFailuresToTolerate":"cc",      # required = false
#       "cachereservation":"dd",            # required = false
#       "fstype":"ee"                       # required = false
#    }
# }

# Custom Create Sample
# {
#    "type":"storageClass",
#    "provisioner":"cdc",
#    "reclaimPolicy":"Delete",
#    "allowVolumeExpansion":false,
#    "volumeBindingMode":"Immediate",
#    "name":null,
#    "parameters":{                     # required = false
#       "aaa":"bbb",
#       "ccc":"ddd",
#       "eee":"fff"
#    }
# }
