import os
from pathlib import Path

from pydicom import dcmread
from pydicom.filewriter import write_file_meta_info
from pydicom.uid import ImplicitVRLittleEndian
from pydicom.dataset import Dataset, FileMetaDataset
from pynetdicom.presentation import build_context

from pynetdicom import AE, VerificationPresentationContexts, build_role, debug_logger, StoragePresentationContexts, evt
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
from move_dicom import move_dcm

debug_logger()


def handle_store(event, directory):
    """
    Handle a C-STORE request event.
    directory - куда сохранять файлы
    """
    with open(f'{directory}\\{event.request.AffectedSOPInstanceUID}.dcm', 'wb') as f:
        # Write the preamble and prefix
        f.write(b'\x00' * 128)
        f.write(b'DICM')
        # Encode and write the File Meta Information
        write_file_meta_info(f, event.file_meta)
        # Write the encoded dataset
        f.write(event.request.DataSet.getvalue())

    # Return a 'Success' status
    return 0x0000


def read_dcm(directory):
    """
    Находит в ORTHANC натроеном без авторизации исследования по модальности MG
    и сохраняет данные первой найденной серии в заданную диреторию
    в дальнейшем можно добавить парсер на другие параметры
    :param directory: директория для сохранения исследований
    :return:
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

    ae = AE(ae_title='ORTHANC')
    seIP = '127.0.0.1'
    sePORT = 4242
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelGet)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
    ae.add_supported_context(Verification)
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(CTImageStorage)
    ae.requested_contexts = StoragePresentationContexts[:120]

    negotiation_items = []
    for context in StoragePresentationContexts[:120]:
        role = build_role(context.abstract_syntax, scp_role=True)
        negotiation_items.append(role)

    role_a = SCP_SCU_RoleSelectionNegotiation()
    role_a.sop_class_uid = CTImageStorage
    role_a.scu_role = True
    role_a.scp_role = True

    negotiation_items.append(role_a)

    role_b = build_role(MRImageStorage, scp_role=True)

    negotiation_items.append(role_b)

    handlers = [(evt.EVT_C_STORE, handle_store, [directory])]

    assoc = ae.associate(seIP, sePORT, ext_neg=negotiation_items, ae_title='ORTHANC', evt_handlers=handlers)

    ds = Dataset()

    ds.file_meta = FileMetaDataset()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds.QueryRetrieveLevel = 'STUDY'
    ds.PatientName = '*'
    ds.PatientID = '*'
    ds.StudyInstanceUID = ''
    ds.SeriesInstanceUID = ''
    ds.ScheduledProcedureStepSequence = [Dataset()]
    item = ds.ScheduledProcedureStepSequence[0]
    # Возможны другие параметры
    # item.ScheduledStationAETitle = 'CTSCANNER'
    # item.ScheduledProcedureStepStartDate = '20181005'
    item.Modality = 'MG'

    my_ds = None

    if assoc.is_established:
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        i = 0
        for (status, identifier) in responses:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))
            print('status = ', status)
            print('identifier = ', identifier)
            if status and identifier:
                i += 1
                if i == 1:
                    my_ds = identifier
            elif status:
                print('status')
                print('##############################')
                print('C-FIND query status: 0x{0:04x}'.format(status.Status))
            elif identifier:
                print('identifier')
            else:
                print('Connection timed out, was aborted or received invalid response')
        print('############# FIND ', i)

        if my_ds:
            responses1 = assoc.send_c_get(my_ds, PatientRootQueryRetrieveInformationModelGet)
            #responses1 = assoc.send_c_get(my_ds, StudyRootQueryRetrieveInformationModelGet)
            for (status1, identifier1) in responses1:
                if status1 and identifier1:
                    print('status = ', status1)
                    print('identifier = ', identifier1)
                else:
                    print('no c_get')

        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


if __name__ == '__main__':
    read_dcm(f'{os.path.dirname(os.path.realpath(__file__))}/dicom_img')
