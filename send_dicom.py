import os
from pathlib import Path

from pydicom import dcmread
from pydicom.uid import ImplicitVRLittleEndian

from pynetdicom import AE, VerificationPresentationContexts, StoragePresentationContexts, build_role  # , debug_logge
from pynetdicom.pdu_primitives import SCP_SCU_RoleSelectionNegotiation
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelGet,
    ProtocolApprovalInformationModelGet,
    BasicWorklistManagementServiceClass,
    CTImageStorage,
    StudyRootQueryRetrieveInformationModelGet,
    MRImageStorage,
    StudyRootQueryRetrieveInformationModelMove,
    PatientRootQueryRetrieveInformationModelMove,
    CompositeInstanceRetrieveWithoutBulkDataGet,
    XRayAngiographicImageStorage,
    Verification
    )

from pydicom.uid import (
    ImplicitVRLittleEndian,
    ExplicitVRLittleEndian,


    ExplicitVRBigEndian)

#debug_logger()


def send_dcm(path_img):
    """
    Отправка dcm файлов на сервер ORTHANC без авторизации
    :param path_img:
    :return:
    """
    Path(path_img).mkdir(parents=True, exist_ok=True)
    #directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    ae = AE(ae_title='ORTHANC')
    seIP = '127.0.0.1'
    sePORT = 4242
    ae.requested_contexts = StoragePresentationContexts
    role_a = SCP_SCU_RoleSelectionNegotiation()
    role_a.sop_class_uid = CTImageStorage
    role_a.scu_role = True
    role_a.scp_role = True

    role_b = build_role(MRImageStorage, scp_role=True)

    assoc = ae.associate(seIP, sePORT, ext_neg=[role_a, role_b], ae_title='ORTHANC')
    if assoc.is_established:
        i = 0
        for file in os.listdir(path_img):
            filename = os.fsdecode(file)
            if filename.endswith(".dcm"):
                open_filename = os.path.join(path_img, filename)
                ds = dcmread(open_filename, force=True)
                # `status` is the response from the peer to the store request
                # but may be an empty pydicom Dataset if the peer timed out or
                # sent an invalid dataset.
                status = assoc.send_c_store(ds)
                i += 1
                if status:
                    # If the storage request succeeded this will be 0x0000
                    print('C-STORE request status: 0x{0:04x}'.format(status.Status))
                else:
                    print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    print(f'Передача {i} изображений завершено!')


if __name__ == '__main__':
    send_dcm(f'{os.path.dirname(os.path.realpath(__file__))}/dicom_new_img')
