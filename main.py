from pprint import pprint
import json
with open('ssdt.dsl', 'r') as f:
    ssdt = f.readlines()

externals = []
methods = []
offsets = []
variables = []
op_regs = []

tree = {}

skipped_fields = (

    '/*',
    '*',
)


for lines in ssdt:
    current_line = lines.strip()
    if current_line.startswith(skipped_fields):
        continue

    if current_line.startswith('DefinitionBlock'):
        print(f"Definition Block stuff:\n\n\tTableSignature: {current_line.split()[2][1:-2]}\n\tComplianceRevision: {current_line.split()[3][:-1]}\n\tOEMID: {current_line.split()[4][1:]}\n\tTableID: {current_line.split()[6][1:]}\n\tOEMRevision: {current_line.split()[8][:-1]}\n")

    if current_line.startswith('External'):
        external_object_name = current_line.split()[1][1:-1]
        external_object_type = current_line.split()[2][0:-1]
        external_object = {
            'name': external_object_name,
            'type': external_object_type
        }
        externals.append(external_object)
        print(f"External reference found! {external_object_name} is a {external_object_type}")


with open('output.json', 'w') as f:
    json.dump(externals, f, indent=4)
    
print(externals)
# for lines in ssdt:
#     current_line = lines.strip()
#     if list(current_line) == []: # skips empty line
#         continue
    
#     if current_line.startswith(skipped_fields):
#         continue

#     if current_line.startswith('External'):
#         external_object_name = current_line.split()[1][1:-1]
#         external_object_type = current_line.split()[2][0:-1]
#         external_object = {
#             'name': external_object_name,
#             'type': external_object_type
#         }
#         externals.append(external_object)
    
#     if current_line.startswith('Name'):
#         print(current_line)
#         var_name = current_line.split()[1][1:-1]
#         var_value = ''
#         match var_name:
#             case '_HID':
#                 if current_line.split()[2].startswith('EisaId'):
#                     var_value = f"EisaId ({current_line.split()[3][1:-1].strip(')')})"
#                 else:
#                     var_value = current_line.split()[2][0:-1].strip(')')

#         var = {
#             'name': var_name,
#             'value': var_value
#         }
#         variables.append(var)

    
# pprint(variables)

    