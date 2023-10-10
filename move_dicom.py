import os

from pydicom import dcmread
from pydicom.filewriter import write_file_meta_info
from pydicom.uid import ImplicitVRLittleEndian
from pydicom.dataset import Dataset, FileMetaDataset

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
    PatientStudyOnlyQueryRetrieveInformationModelMove,
    CompositeInstanceRetrieveWithoutBulkDataGet,
    XRayAngiographicImageStorage,
    #SeriesRootQueryRetrieveInformationModelMove,
    Verification
    )

from pydicom.uid import (
    ImplicitVRLittleEndian,
    ExplicitVRLittleEndian,


    ExplicitVRBigEndian)

debug_logger()


def handle_store(event):
    """Handle a C-STORE service request"""
    # Ignore the request and return Success
    with open(f'C:\\Users\\slava\\Documents\\python\\Dicom\\dicom_img_1\\{event.request.AffectedSOPInstanceUID}.dcm',
              'wb') as f:
        # Write the preamble and prefix
        f.write(b'\x00' * 128)
        f.write(b'DICM')
        # Encode and write the File Meta Information
        write_file_meta_info(f, event.file_meta)
        # Write the encoded dataset
        f.write(event.request.DataSet.getvalue())

    # Return a 'Success' status
    return 0x0000



#def move_dcm(my_ds):
def move_dcm(directory, study_instance_uid):
    #directory = os.fsdecode(os.fsencode(os.path.dirname(os.path.realpath(__file__)))) + '\\' + path_img
    ae = AE(ae_title='ORTHANC') # RADIANT1 140 PYNETDICOM
    seIP = '127.0.0.1'
    sePORT = 4242
    # We can also do the same thing with the requested contexts
    #ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
    #ae.add_requested_context(StudyRootQueryRetrieveInformationModelGet)
    #ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
    #ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
    #ae.add_requested_context(PatientStudyOnlyQueryRetrieveInformationModelMove)
    ae.add_supported_context(Verification)
    ae.add_requested_context(MRImageStorage)

    ae.add_requested_context(CTImageStorage)
    #ae.add_requested_context(
    #    MRImageStorage, [ImplicitVRLittleEndian, ExplicitVRLittleEndian]
    #)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
    #ae.add_requested_context(SeriesRootQueryRetrieveInformationModelMove)

    ae.supported_contexts = StoragePresentationContexts

    negotiation_items = []
    for context in StoragePresentationContexts[:120]:
        role = build_role(context.abstract_syntax, scp_role=True)
        negotiation_items.append(role)

    role_a = SCP_SCU_RoleSelectionNegotiation()
    role_a.sop_class_uid = CTImageStorage
    role_a.scu_role = True
    role_a.scp_role = True

    #role_b = build_role(MRImageStorage, scp_role=True, role_a.scu_role = True)
    role_b = SCP_SCU_RoleSelectionNegotiation()
    role_b.sop_class_uid = CTImageStorage
    role_b.scu_role = True
    role_b.scp_role = True

    ext_neg = []
    uids = ['1.2.840.10008.5.1.4.1.2.1.3', '1.2.840.10008.5.1.4.1.1.1.2']
    for uid in uids:
        tmp = SCP_SCU_RoleSelectionNegotiation()
        tmp.sop_class_uid = uid
        tmp.scu_role = True
        tmp.scp_role = True

        negotiation_items.append(tmp)
        ae.add_supported_context(uid)

    #handlers = [(evt.EVT_C_MOVE, handle_move)]
    handlers = [(evt.EVT_C_STORE, handle_store)]

    #ae.start_server(('127.0.0.1', 11112), block=False, evt_handlers=handlers)

    #assoc = ae.associate(seIP, 4242, ext_neg=[role_a, role_b], ae_title='ORTHANC')
    #assoc = ae.associate(seIP, 4242, ae_title='ORTHANC')
    assoc = ae.associate(seIP, 4242, ext_neg=negotiation_items, ae_title='ORTHANC', evt_handlers=handlers)
    #assoc = ae.associate(seIP, 4242, ext_neg=[role_a, role_b], ae_title='ORTHANC')



    ds = Dataset()
    # ds=dicom.dcmread(path)


    ds.file_meta = FileMetaDataset()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds.QueryRetrieveLevel = 'STUDY' #'STUDY' #'SERIES' PATIENT
    #ds = my_ds


    #ds.PatientName = '*'
    ds.PatientID = '*' #'d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f' #'d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f'
    ds.StudyInstanceUID = study_instance_uid
    #ds.StudyInstanceUID = '1.2.276.0.7230010.3.1.2.3252257021.10392.1690202165.1214'


    ds.PatientName = '*'
    ds.Modality = '*'
    #ds.StudyInstanceUID = '*'
    ds.SeriesInstanceUID = '*'
    #ds.is_little_endian = True
    #.is_implicit_VR = True
    #ds.SeriesInstanceUID = '1.2.276.0.7230010.3.1.3.3252257021.10392.1690202165.1188'
    # ds.QueryRetrieveLevel = 'STUDY'
    #ds.ScheduledProcedureStepSequence = [Dataset()]
    #item = ds.ScheduledProcedureStepSequence[0]
    #item.StudyInstanceUID = study_instance_uid
    # item.ScheduledStationAETitle = 'CTSCANNER'
    # item.ScheduledProcedureStepStartDate = '20181005'
    # ds.StudyInstanceUID = "1.2.276.0.7230010.3.1.2.3252257021.10392.1690202165.1214"
    #item.Modality = 'MG'
    #item.StudyDateDA = ''
    #item.StudyTimeTM = ''

    #suffix = '.dmc'
    #fpath = directory + ds.StudyInstanceUID + suffix
    #ds.save_as(fpath, write_like_original=False)
    #ds.file_meta = FileMetaDataset()
    #ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    #ds.save_as(directory)


    if assoc.is_established:
        for cx in assoc.accepted_contexts:
            cx._as_scp = True

        print('TEST 944960 assoc.is_established ')
        is_established = 'Y'
        print('TEST 416830 send_c_move ')
        # responses = assoc.send_c_move(ds,
        #    query_model=MRImageStorage,
        #    move_aet=myAETITE,
        #    )
        #responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        #responses = assoc.send_c_move(ds, 'ORTHANC', StudyRootQueryRetrieveInformationModelMove)
        responses = assoc.send_c_move(ds, 'ORTHANC', PatientRootQueryRetrieveInformationModelMove)
        #responses = assoc.send_c_move(ds, 'ORTHANC', PatientStudyOnlyQueryRetrieveInformationModelMove)
        #responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
        #responses = assoc.send_c_move(ds, 'RADIANT', SeriesRootQueryRetrieveInformationModelMove)
        #responses = assoc.send_c_move(ds,
        #                             query_model=CTImageStorage,
        #                             move_aet='RADIANT',
        #                             )
        print('TEST 459893 before in responses ')
        # print('my test', responses.__next__())
        i = 0
        my_key = None
        for (status, identifier) in responses:
            # UID_plan.add(identifier.SeriesInstanceUID)
            print('TEST 454379 after in responses')
            hresponses = 'Y'

            if status and identifier:
                i += 1
                print('##############################')
                print('C-FIND query status: 0x{0:04x}'.format(status.Status))
                # print(identifier.PatientID)
                print(identifier.PatientName)
                # print(ds.StudyInstanceUID)
                # print(ds.SeriesInstanceUID)
                print('status = ', status)
                print('type(status) = ', type(status))
                print('status.Status = ', status.Status)
                print('type(identifier) = ', type(identifier))
                print('identifier = ', identifier)
                print('status.keys()  = ', status.keys())
                print('identifier.keys()  = ', identifier.keys())
                if not my_key:
                    my_key = status.keys()
                print('status.items()  = ', status.items())
                for elem in identifier.elements():
                    print('elem = ', elem)
                if status.Status in (0xff00, 0xff01):
                    print(identifier)
                print('##############################')
            elif status:
                print('status')
                print('##############################')
                print('C-FIND query status: 0x{0:04x}'.format(status.Status))
                # print(identifier.PatientID)
                #print(identifier.PatientName)
                # print(identifier.StudyInstanceUID)
                # print(identifier.SeriesInstanceUID)
                print('status = ', status)
                print('type(status) = ', type(status))
                print('status.Status = ', status.Status)
            elif identifier:
                print('identifier')
            else:
                print('Connection timed out, was aborted or received invalid response')
        print('############# FIND ', i)
        # for cx in assoc.accepted_contexts:
        #    cx._as_scp = True
        # responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
        # for (status, identifier) in responses:
        #    if status:
        #        print('C-GET query status: 0x{0:04x}'.format(status.Status))
        #    else:
        #        print('Connection timed out, was aborted or received invalid response')

        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
    #print("Number of plans found : " + str(len(UID_plan)))
    #print(UID_plan)


if __name__ == '__main__':
    move_dcm('dicom_img', '1.2.276.0.7230010.3.1.2.3252257021.10392.1690202165.1187')
    #pass
