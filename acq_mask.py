#!/usr/bin/python
#
# Acquistion mask for use with usgs_downloader.py. See PDGS-LDCM-CGI-TN-18-1986 for description.
# The mask below is reduced compared to the full station coverage. 
ACQ_MASK = [
    {'wrsPath': '168', 'startRow': '19', 'endRow': '39'},
    {'wrsPath': '169', 'startRow': '17', 'endRow': '39'},
    {'wrsPath': '170', 'startRow': '17', 'endRow': '40'},
    {'wrsPath': '171', 'startRow': '14', 'endRow': '41'},
    {'wrsPath': '172', 'startRow': '14', 'endRow': '42'},
    {'wrsPath': '173', 'startRow': '13', 'endRow': '44'},
    {'wrsPath': '174', 'startRow': '13', 'endRow': '45'},
    {'wrsPath': '175', 'startRow': '12', 'endRow': '46'},
    {'wrsPath': '176', 'startRow': '12', 'endRow': '46'},
    {'wrsPath': '177', 'startRow': '11', 'endRow': '47'},
    {'wrsPath': '178', 'startRow': '11', 'endRow': '47'},
    {'wrsPath': '179', 'startRow': '11', 'endRow': '47'},
    {'wrsPath': '180', 'startRow': '11', 'endRow': '47'},
    {'wrsPath': '181', 'startRow': '11', 'endRow': '47'},
    {'wrsPath': '182', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '183', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '184', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '185', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '186', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '187', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '188', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '189', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '190', 'startRow': '10', 'endRow': '46'},
    {'wrsPath': '191', 'startRow': '10', 'endRow': '45'},
    {'wrsPath': '192', 'startRow': '9', 'endRow': '45'},
    {'wrsPath': '193', 'startRow': '9', 'endRow': '45'},
    {'wrsPath': '194', 'startRow': '9', 'endRow': '44'},
    {'wrsPath': '195', 'startRow': '9', 'endRow': '44'},
    {'wrsPath': '196', 'startRow': '9', 'endRow': '44'},
    {'wrsPath': '197', 'startRow': '9', 'endRow': '43'},
    {'wrsPath': '198', 'startRow': '9', 'endRow': '42'},
    {'wrsPath': '199', 'startRow': '10', 'endRow': '42'},
    {'wrsPath': '200', 'startRow': '10', 'endRow': '41'},
    {'wrsPath': '201', 'startRow': '10', 'endRow': '40'},
    {'wrsPath': '202', 'startRow': '6', 'endRow': '40'},
    {'wrsPath': '203', 'startRow': '20', 'endRow': '41'},
    {'wrsPath': '204', 'startRow': '19', 'endRow': '41'},
    {'wrsPath': '205', 'startRow': '17', 'endRow': '41'},
    {'wrsPath': '206', 'startRow': '17', 'endRow': '41'},
    {'wrsPath': '207', 'startRow': '18', 'endRow': '41'},
    {'wrsPath': '208', 'startRow': '18', 'endRow': '41'},
    {'wrsPath': '209', 'startRow': '16', 'endRow': '24'},
    {'wrsPath': '210', 'startRow': '16', 'endRow': '17'},
    {'wrsPath': '215', 'startRow': '14', 'endRow': '15'},
    {'wrsPath': '216', 'startRow': '9', 'endRow': '16'},
    {'wrsPath': '217', 'startRow': '9', 'endRow': '16'},
    {'wrsPath': '218', 'startRow': '9', 'endRow': '16'},
    {'wrsPath': '219', 'startRow': '13', 'endRow': '16'},
    {'wrsPath': '220', 'startRow': '13', 'endRow': '16'},
    {'wrsPath': '221', 'startRow': '13', 'endRow': '15'},
    {'wrsPath': '222', 'startRow': '13', 'endRow': '15'},
    {'wrsPath': '223', 'startRow': '12', 'endRow': '14'}
]
"""
The acquisition mask below represents the full combined coverage of Matera and Kiruna stations.
It is included here for reference.
ACQ_MASK = [
    {'wrsPath': '1', 'startRow': '4', 'endRow': '14'},
    {'wrsPath': '2', 'startRow': '3', 'endRow': '14'},
    {'wrsPath': '3', 'startRow': '3', 'endRow': '14'},
    {'wrsPath': '4', 'startRow': '3', 'endRow': '14'},
    {'wrsPath': '5', 'startRow': '2', 'endRow': '13'},
    {'wrsPath': '6', 'startRow': '2', 'endRow': '13'},
    {'wrsPath': '7', 'startRow': '2', 'endRow': '13'},
    {'wrsPath': '8', 'startRow': '2', 'endRow': '12'},
    {'wrsPath': '9', 'startRow': '1', 'endRow': '12'},
    {'wrsPath': '10', 'startRow': '1', 'endRow': '12'},
    {'wrsPath': '11', 'startRow': '1', 'endRow': '11'},
    {'wrsPath': '12', 'startRow': '1', 'endRow': '11'},
    {'wrsPath': '13', 'startRow': '1', 'endRow': '10'},
    {'wrsPath': '14', 'startRow': '1', 'endRow': '10'},
    {'wrsPath': '15', 'startRow': '1', 'endRow': '10'},
    {'wrsPath': '16', 'startRow': '1', 'endRow': '9'},
    {'wrsPath': '17', 'startRow': '1', 'endRow': '9'},
    {'wrsPath': '18', 'startRow': '1', 'endRow': '8'},
    {'wrsPath': '19', 'startRow': '1', 'endRow': '8'},
    {'wrsPath': '20', 'startRow': '1', 'endRow': '7'},
    {'wrsPath': '21', 'startRow': '1', 'endRow': '7'},
    {'wrsPath': '22', 'startRow': '1', 'endRow': '7'},
    {'wrsPath': '23', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '24', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '25', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '26', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '27', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '28', 'startRow': '1', 'endRow': '6'},
    {'wrsPath': '29', 'startRow': '1', 'endRow': '5'},
    {'wrsPath': '31', 'startRow': '1', 'endRow': '5'},
    {'wrsPath': '32', 'startRow': '1', 'endRow': '4'},
    {'wrsPath': '33', 'startRow': '1', 'endRow': '5'},
    {'wrsPath': '34', 'startRow': '1', 'endRow': '4'},
    {'wrsPath': '35', 'startRow': '1', 'endRow': '4'},
    {'wrsPath': '151', 'startRow': '5', 'endRow': '15'},
    {'wrsPath': '152', 'startRow': '4', 'endRow': '16'},
    {'wrsPath': '153', 'startRow': '4', 'endRow': '17'},
    {'wrsPath': '154', 'startRow': '4', 'endRow': '18'},
    {'wrsPath': '155', 'startRow': '4', 'endRow': '19'},
    {'wrsPath': '156', 'startRow': '4', 'endRow': '20'},
    {'wrsPath': '157', 'startRow': '3', 'endRow': '20'},
    {'wrsPath': '158', 'startRow': '3', 'endRow': '21'},
    {'wrsPath': '159', 'startRow': '3', 'endRow': '22'},
    {'wrsPath': '160', 'startRow': '3', 'endRow': '22'},
    {'wrsPath': '161', 'startRow': '3', 'endRow': '23'},
    {'wrsPath': '162', 'startRow': '3', 'endRow': '24'},
    {'wrsPath': '163', 'startRow': '1', 'endRow': '24'},
    {'wrsPath': '164', 'startRow': '1', 'endRow': '25'},
    {'wrsPath': '165', 'startRow': '1', 'endRow': '25'},
    {'wrsPath': '166', 'startRow': '1', 'endRow': '25'},
    {'wrsPath': '167', 'startRow': '1', 'endRow': '25'},
    {'wrsPath': '168', 'startRow': '1', 'endRow': '38'},
    {'wrsPath': '169', 'startRow': '1', 'endRow': '39'},
    {'wrsPath': '170', 'startRow': '8', 'endRow': '40'},
    {'wrsPath': '171', 'startRow': '11', 'endRow': '41'},
    {'wrsPath': '172', 'startRow': '10', 'endRow': '43'},
    {'wrsPath': '173', 'startRow': '10', 'endRow': '44'},
    {'wrsPath': '174', 'startRow': '1', 'endRow': '45'},
    {'wrsPath': '175', 'startRow': '5', 'endRow': '46'},
    {'wrsPath': '176', 'startRow': '2', 'endRow': '46'},
    {'wrsPath': '177', 'startRow': '2', 'endRow': '47'},
    {'wrsPath': '178', 'startRow': '2', 'endRow': '47'},
    {'wrsPath': '179', 'startRow': '2', 'endRow': '47'},
    {'wrsPath': '180', 'startRow': '1', 'endRow': '47'},
    {'wrsPath': '181', 'startRow': '5', 'endRow': '47'},
    {'wrsPath': '182', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '183', 'startRow': '12', 'endRow': '46'},
    {'wrsPath': '184', 'startRow': '12', 'endRow': '46'},
    {'wrsPath': '185', 'startRow': '12', 'endRow': '46'},
    {'wrsPath': '186', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '187', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '188', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '189', 'startRow': '11', 'endRow': '46'},
    {'wrsPath': '190', 'startRow': '10', 'endRow': '46'},
    {'wrsPath': '191', 'startRow': '2', 'endRow': '45'},
    {'wrsPath': '192', 'startRow': '1', 'endRow': '45'},
    {'wrsPath': '193', 'startRow': '1', 'endRow': '45'},
    {'wrsPath': '194', 'startRow': '1', 'endRow': '44'},
    {'wrsPath': '195', 'startRow': '1', 'endRow': '44'},
    {'wrsPath': '196', 'startRow': '1', 'endRow': '44'},
    {'wrsPath': '197', 'startRow': '1', 'endRow': '43'},
    {'wrsPath': '198', 'startRow': '1', 'endRow': '42'},
    {'wrsPath': '199', 'startRow': '1', 'endRow': '42'},
    {'wrsPath': '200', 'startRow': '1', 'endRow': '41'},
    {'wrsPath': '201', 'startRow': '1', 'endRow': '40'},
    {'wrsPath': '202', 'startRow': '1', 'endRow': '40'},
    {'wrsPath': '203', 'startRow': '1', 'endRow': '38'},
    {'wrsPath': '204', 'startRow': '1', 'endRow': '35'},
    {'wrsPath': '205', 'startRow': '1', 'endRow': '32'},
    {'wrsPath': '206', 'startRow': '1', 'endRow': '24'},
    {'wrsPath': '207', 'startRow': '2', 'endRow': '25'},
    {'wrsPath': '208', 'startRow': '2', 'endRow': '24'},
    {'wrsPath': '209', 'startRow': '2', 'endRow': '24'},
    {'wrsPath': '210', 'startRow': '2', 'endRow': '17'},
    {'wrsPath': '211', 'startRow': '2', 'endRow': '5'},
    {'wrsPath': '212', 'startRow': '2', 'endRow': '5'},
    {'wrsPath': '213', 'startRow': '2', 'endRow': '5'},
    {'wrsPath': '214', 'startRow': '2', 'endRow': '5'},
    {'wrsPath': '215', 'startRow': '2', 'endRow': '15'},
    {'wrsPath': '216', 'startRow': '2', 'endRow': '16'},
    {'wrsPath': '217', 'startRow': '2', 'endRow': '16'},
    {'wrsPath': '218', 'startRow': '2', 'endRow': '16'},
    {'wrsPath': '219', 'startRow': '2', 'endRow': '16'},
    {'wrsPath': '220', 'startRow': '2', 'endRow': '16'},
    {'wrsPath': '221', 'startRow': '2', 'endRow': '15'},
    {'wrsPath': '222', 'startRow': '2', 'endRow': '15'},
    {'wrsPath': '223', 'startRow': '2', 'endRow': '14'},
    {'wrsPath': '225', 'startRow': '9', 'endRow': '12'},
    {'wrsPath': '226', 'startRow': '7', 'endRow': '12'},
    {'wrsPath': '227', 'startRow': '6', 'endRow': '12'},
    {'wrsPath': '228', 'startRow': '6', 'endRow': '13'},
    {'wrsPath': '229', 'startRow': '5', 'endRow': '13'},
    {'wrsPath': '230', 'startRow': '5', 'endRow': '14'},
    {'wrsPath': '231', 'startRow': '5', 'endRow': '14'},
    {'wrsPath': '232', 'startRow': '5', 'endRow': '15'},
    {'wrsPath': '233', 'startRow': '4', 'endRow': '15'}
]
"""