from pprint import pprint
import sys

sys.setrecursionlimit(5000)
with open('ssdt.dsl', 'r') as f:
    ssdt = f.readlines()


    externals = []
    methods = []
    offsets = []
    variables = []
    op_regs = []

    tree = {'DSDT': {}}
    tree['DSDT']['Devices'] = []
    tree['DSDT']['Methods'] = []
    tree['DSDT']['Names'] = []
    tree['DSDT']['OpRegs'] = []

    skipped_fields = (

        '/*',
        '*',
        '//',
    )

    current_scope = ''

    for lines in ssdt:
        current_line = lines.strip()

        if current_line.startswith(skipped_fields):
            continue

        if current_line.startswith('DefinitionBlock'):
            print(f"\nDefinition Block stuff:\n\n\tTableSignature: {current_line.split()[2][1:-2]}\n\tComplianceRevision: {current_line.split()[3][:-1]}\n\tOEMID: {current_line.split()[4][1:]}\n\tTableID: {current_line.split()[6][1:]}\n\tOEMRevision: {current_line.split()[8][:-1]}\n")

        if current_line.startswith('External'):
            external_object_name = current_line.split()[1][1:-1]
            external_object_type = current_line.split()[2][0:-1]
            external_object = {
                'name': external_object_name,
                'type': external_object_type
            }
            externals.append(external_object)
        
        if current_line.startswith('Name'):
            var_name = current_line.split()[1][1:-1]
            var_value = ''
            match var_name:
                case '_HID':
                    if current_line.split()[2].startswith('EisaId'):
                        var_value = f"EisaId ({current_line.split()[3][1:-1].strip(')')})"
                    else:
                        var_value = current_line.split()[2][0:-1].strip(')')
                case _:
                    var_value = current_line.split()[-1][:-1]

        if current_line.startswith('Scope'):
            current_scope = current_line.strip().split()[1][1:-1].split('.') #will be a list
            current_object = tree

            for breadcrumb in current_scope:
                try:
                    current_object = current_object[breadcrumb]
                except KeyError:
                    current_object[breadcrumb] = dict()
                    current_object = current_object[breadcrumb]
            
            last_scope = current_object
        
        if current_line.startswith('Device'):
            device_name = current_line.strip().split()[1][1:-1]
            current_object = tree
            for breadcrumb in current_scope:
                current_object = current_object[breadcrumb]
                if breadcrumb == current_scope[-1]:
                    current_object[device_name] = dict()
    pprint(tree)

    