# have prototypes instead
#
import os
import json
import Record
import Tags

#data
# item_categories = Record.Sender('packaging')
# item_categories.populateData( item_categories.GetFromApi('items-categories'), None)
# item_categories = item_categories.data
#
# package_types = Record.Sender('packaging')
# package_types.populateData( package_types.GetFromApi('packages-types'), None)
# package_types = package_types.data

DATA_DICT = {
    'room_name': 'MK Plants Room'
    , 'room_name_updated': 'MK Plants Room Updated'
    , 'strain_name1': 'MK Charlotte'
    , 'strain_name2': 'MK Yiyan'
    , 'plantbatch_name1': 'MK Cindy Test'
    , 'plantbatch_name2': 'MK Ravi Test'
    , 'plantbatch_name3': 'MK Cynthia Test'
    , 'strain_testing_status': 'None'
    , 'mantissa1': 0.075
    , 'mantissa2': 0.14
    , 'percent1': 25.0
    , 'percent2': 75.0
    , 'decimal1': 1.0
    , 'integer1': 25
    , 'unit_of_weight1': 'Grams'
    , 'unit_of_weight2': 'Ounces'
    , 'date_str1': '2018-03-12'
    , 'item_category1': 'Edible'
    , 'item_category2': 'Concentrate (solid)'
    , 'item_name1': 'MK Item'
    , 'item_name2': 'Awesome MK Item'
    , 'item_name3': 'Best MK Item'
}


# Rooms
# create new room and return name
new_room = Record.Sender('packaging')
new_room.PopulateData([{'Name': DATA_DICT.get('room_name')}], None)
new_room.SendToApi('rooms-create', new_room.data, ['Name'])

# update name of existing room
new_room.FilterReceivedData('rooms-read', None, new_room.data, ['Id','Name'])
new_room.UpdateFilteredData([{'Name': DATA_DICT.get('room_name_updated')}])
new_room.SendToApi('rooms-update', new_room.filtered_data, ['Name'])


# Strains
# create new strain
new_strain = Record.Sender('packaging')
new_strain.PopulateData([{
    'Name': DATA_DICT.get('strain_name1')
    , 'TestingStatus': DATA_DICT.get('strain_testing_status')
    , 'ThcLevel': DATA_DICT.get('mantissa1')
    , 'CbdLevel': DATA_DICT.get('mantissa2')
    , 'IndicaPercentage': DATA_DICT.get('percent1')
    , 'SativaPercentage': DATA_DICT.get('percent2')
}], None)
new_strain.SendToApi('strains-create', new_strain.data, ['Name'])

# update strain's THC and CBD levels
new_strain.FilterReceivedData('strains-read', None, [{
    'Name': DATA_DICT.get('strain_name1')}], ['Id','Name','TestingStatus','ThcLevel','CbdLevel', 'IndicaPercentage', 'SativaPercentage'])
new_strain.UpdateFilteredData([{'ThcLevel': DATA_DICT.get('mantissa2'), 'CbdLevel': DATA_DICT.get('mantissa1')}])
new_strain.SendToApi('strains-update', new_strain.filtered_data, ['Name'])


# Plant Batches
new_batch = Record.Sender('packaging')
new_batch.PopulateData([
    {
        'Name': DATA_DICT.get('plantbatch_name1')
        , 'Type': 'Seed'
        , 'Count': DATA_DICT.get('integer1')
        , 'Strain': DATA_DICT.get('strain_name1')
        , 'ActualDate': DATA_DICT.get('date_str1')
    }
    , {
        'Name': DATA_DICT.get('plantbatch_name2')
        , 'Type': 'Seed'
        , 'Count': DATA_DICT.get('integer1')
        , 'Strain': DATA_DICT.get('strain_name1')
        , 'ActualDate': DATA_DICT.get('date_str1')
    }
    , {
        'Name': DATA_DICT.get('plantbatch_name3')
        , 'Type': 'Seed'
        , 'Count': DATA_DICT.get('integer1')
        , 'Strain': DATA_DICT.get('strain_name1')
        , 'ActualDate': DATA_DICT.get('date_str1')
    }
], None)
new_batch.SendToApi('plantbatches-create', new_batch.data, ['Name'])

# change growth phase of batch
new_batch.FilterReceivedData('plantbatches-read', None, [{'Name': DATA_DICT.get('plantbatch_name1')},{'Name': DATA_DICT.get('plantbatch_name2')}], ['Id', 'Name', 'Count'])
new_batch.UpdateFilteredData([
    {
        'StartingTag': Tags.PLANT_TAGS_PACKAGING[150]
        , 'GrowthPhase': 'Vegetative'
        , 'NewRoom': DATA_DICT.get('room_name')
        , 'GrowthDate': DATA_DICT.get('date_str1')
    }
    , {
        'StartingTag': Tags.PLANT_TAGS_PACKAGING[151]
        , 'GrowthPhase': 'Vegetative'
        , 'NewRoom': DATA_DICT.get('room_name')
        , 'GrowthDate': DATA_DICT.get('date_str1')
    }
])
new_batch.SendToApi('plantbatches-changegrowth', new_batch.filtered_data, ['Name'])

# destroy 1 of the plants
new_batch.FilterReceivedData('plantbatches-read', None, [{'Name': DATA_DICT.get('plantbatch_name3')}], ['Id', 'Count', 'Name'])
new_batch.UpdateFilteredData([
    {
        'ReasonNote': 'Ran over plants'
        , 'ActualDate': DATA_DICT.get('date_str1')
    }
])
new_batch.SendToApi('plantbatches-delete', new_batch.filtered_data, ['Name'])


# Harvests
# create a package from a harvest
new_harvest = Record.Sender('packaging')
new_harvest.PopulateData(new_harvest.GetFromApi('harvests-read'), 1)
new_harvest.UpdateData([{
    'Harvest': new_harvest.data[0]['Id']
    , 'HarvestRoom': None
    , 'Item': DATA_DICT.get('item_name2')
    , 'Weight': DATA_DICT.get('decimal1')
    , 'UnitOfWeight': DATA_DICT.get('unit_of_weight1')
    , 'Tag': Tags.PACKAGE_TAGS_PACKAGING[69]
    , 'IsProductionBatch': False
    , 'ProductionBatchNumber': None
    , 'ProductionRequiresMediation': False
    , 'RemediateProduct': False
    , 'RemediationMethodId': None
    , 'RemediationDate': None
    , 'RemediationSteps': None
    , 'ActualDate': DATA_DICT.get('date_str1')
}])
new_harvest.SendToApi('harvests-createpackages', new_harvest.data, ['Tag'])


# Items
# create an item
new_item = Record.Sender('packaging')

new_item.PopulateData([{
    'ItemCategory': DATA_DICT.get('item_category1'),
    'Name': DATA_DICT.get('item_name3'),
    'UnitOfMeasure': DATA_DICT.get('unit_of_weight2'),
    'Strain': DATA_DICT.get('strain_name1'),
    'UnitThcContent': None,
    'UnitThcContentUnitOfMeasure': None,
    'UnitVolume': None,
    'UnitVolumeUnitOfMeasure': None,
    'UnitWeight': None,
    'UnitWeightUnitOfMeasure': None
  }
  , {
      'ItemCategory': DATA_DICT.get('item_category2'),
      'Name': DATA_DICT.get('item_name3'),
      'UnitOfMeasure': DATA_DICT.get('unit_of_weight2'),
      'Strain': DATA_DICT.get('strain_name1'),
      'UnitThcContent': None,
      'UnitThcContentUnitOfMeasure': None,
      'UnitVolume': None,
      'UnitVolumeUnitOfMeasure': None,
      'UnitWeight': None,
      'UnitWeightUnitOfMeasure': None
    }
], None)
new_item.SendToApi('items-create', new_item.data, ['Name'])

new_item.FilterReceivedData('items-read', None, [{'Name': DATA_DICT.get('item_name2')}], ['Id', 'Name', 'UnitThcContent', 'UnitVolume', 'UnitWeight'])
new_item.UpdateFilteredData([{
      'Strain': DATA_DICT.get('strain_name1'),
      'ItemCategory': DATA_DICT.get('item_category2'),
      'UnitOfMeasure': DATA_DICT.get('unit_of_weight1'),
      'UnitThcContentUnitOfMeasure': None,
      'UnitVolumeUnitOfMeasure': None,
      'UnitWeightUnitOfMeasure': None
}])
new_item.SendToApi('items-update', new_item.filtered_data, ['Name'])
