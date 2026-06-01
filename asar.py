# -*- coding: utf-8 -*-
import json
import os
import struct

def read_asar(asar_path: str):
    """Read ASAR file, return (header_dict, data_offset, raw_data_bytes)."""
    with open(asar_path, 'rb') as f:
        pickle_size = struct.unpack('<I', f.read(4))[0]
        header_data_size = struct.unpack('<I', f.read(4))[0]
        header_string_size = struct.unpack('<I', f.read(4))[0]
        actual_json_size = struct.unpack('<I', f.read(4))[0]
        
        header_json = f.read(actual_json_size).decode('utf-8')
        header = json.loads(header_json)
        
        data_offset = 8 + header_data_size
        f.seek(data_offset)
        data = f.read()
        
    return header, data_offset, data

def write_asar(asar_path: str, header: dict, file_contents: dict):
    """
    Write a new ASAR file.
    header: the ASAR header dict (will be updated with new offsets/sizes)
    file_contents: dict of {path: bytes} for files to write
    """
    current_offset = 0
    ordered_files = []
    
    def update_node(node, prefix=''):
        nonlocal current_offset
        if 'files' in node:
            for name in sorted(node['files'].keys()):
                child = node['files'][name]
                path = f"{prefix}/{name}" if prefix else name
                update_node(child, path)
        elif 'offset' in node and not node.get('unpacked'):
            path = prefix
            if path in file_contents:
                data = file_contents[path]
            else:
                data = file_contents.get(path, b'')
            
            node['offset'] = str(current_offset)
            node['size'] = len(data)
            ordered_files.append((path, data))
            current_offset += len(data)
    
    update_node(header)
    
    header_json = json.dumps(header, separators=(',', ':'), ensure_ascii=False)
    header_bytes = header_json.encode('utf-8')
    header_string_size = len(header_bytes)
    
    padding = (4 - (header_string_size % 4)) % 4
    header_bytes_padded = header_bytes + b'\x00' * padding
    header_string_size_padded = 4 + len(header_bytes_padded)
    header_data_size = 4 + header_string_size_padded

    with open(asar_path, 'wb') as f:
        f.write(struct.pack('<I', 4))
        f.write(struct.pack('<I', header_data_size))
        f.write(struct.pack('<I', header_string_size_padded))
        f.write(struct.pack('<I', header_string_size))
        f.write(header_bytes_padded)
        
        for path, data in ordered_files:
            f.write(data)

def collect_all_files(header: dict, data: bytes, prefix='') -> dict:
    """Collect all non-unpacked file contents from ASAR data."""
    result = {}
    if 'files' in header:
        for name, child in header['files'].items():
            path = f"{prefix}/{name}" if prefix else name
            result.update(collect_all_files(child, data, path))
    elif 'offset' in header and not header.get('unpacked'):
        offset = int(header['offset'])
        size = int(header['size'])
        result[prefix] = data[offset:offset + size]
    return result
