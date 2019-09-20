class Tag:
    def __init__(self, tag_dict):
        keys = tag_dict.keys()
        
        if 'tag' in keys:
            self.tag = tag_dict['tag']
            end_tag = self.tag.split(' ')[0]
            self.end_tag = end_tag[:1] + '/' + end_tag[1:]
            if self.end_tag[-1] != '>':
                self.end_tag += '>'
        else:
            self.tag = ''
            self.end_tag = ''
       
        if 'tags' in keys:
            if self.tag == '<tbody>':
                self.tags = [RowTag(tag) for tag in tag_dict['tags']]
            else:
                self.tags = [Tag(tag) for tag in tag_dict['tags']]
        else:
            self.tags = []

        if 'text' in keys:
            self.text = tag_dict['text']
        else:
            self.text = ''

        if 'on_next' in keys:
            self.on_next = tag_dict['on_next']
        else:
            self.on_next = ''
    
    def generate(self, stack, data_frame):
        intend = len(stack) * '\t'
        if self.tag == '<tbody>':
            ret = ''
            for _, data_row in data_frame.iterrows():
                ret += intend + self.tag + self.text + '\n'
                stack.append(self.end_tag)
                for tag in self.tags:
                    ret += tag.generate(stack, data_row)
                end_tag = stack.pop()
                ret += intend + end_tag + '\n'
            return ret
        else:
            ret = intend + self.tag + self.text + '\n'
            stack.append(self.end_tag)
            for tag in self.tags:
                ret += tag.generate(stack, data_frame)
            end_tag = stack.pop()
            ret += intend + end_tag + '\n'
            return ret


class RowTag:
    def __init__(self, tag_dict):
        keys = tag_dict.keys()
        self.tag = tag_dict['tag']

        end_tag = self.tag.split(' ')[0]
        self.end_tag = end_tag[:1] + '/' + end_tag[1:]
        if self.end_tag[-1] != '>':
            self.end_tag += '>'
        
        if 'tags' in keys:
            self.tags = [RowTag(tag) for tag in tag_dict['tags']]
        else:
            self.tags = []
        
        if 'text' in keys:
            self.text = tag_dict['text']
        else:
            self.text = ''

        if 'on_next' in keys:
            self.on_next = tag_dict['on_next']
        else:
            self.on_next = ''
        
        if 'fields' in keys:
            self.fields = [Field(field) for field in tag_dict['fields']]
        else:
            self.fields = []

    def generate(self, stack, data_row):
        intend = len(stack) * '\t'
        ret = intend + self.tag + self.text + '\n'
        stack.append(self.end_tag)

        for tag in self.tags:
            ret += tag.generate(stack, data_row)

        if len(self.fields) > 1 and self.on_next != '':
            for field in self.fields:
                generated_field = field.generate(data_row)
                if generated_field != '':
                    ret += intend + '\t' + generated_field + '\n'
                    ret += intend + '\t' + self.on_next + '\n'
            ret = ret[:-(len(self.on_next) + len(intend) + 3)] + '\n'
        else:
            for field in self.fields:
                ret += intend + '\t' + field.generate(data_row) + '\n'
        end_tag = stack.pop()
        ret += intend + end_tag + '\n'
        return ret


class Clartable(Tag):
    def __init__(self, tag):
        super().__init__(tag)
        self.tag_stack = []

    def generate(self, data_frame):
        ret = ''
        for tag in self.tags:
            ret += tag.generate(self.tag_stack, data_frame)
        return ret

class Field:
    def __init__(self, field_dict):
        self.optional = field_dict['optional']
        self.text = field_dict['text']
        self.columns = field_dict['columns']

    def generate(self, data_row):
        fields_data = [data_row[column] for column in self.columns]
        if self.optional:
            for field_data in fields_data:
                if field_data == '':
                    return ''
        #if len(fields_data) > 1:
            #fields_data = tuple(fields_datas)
        print(self.text)
        print(fields_data)
        if len(fields_data) > 1:
            fields_data = tuple(fields_data)
        else:
            fields_data = fields_data[0]

        return self.text % fields_data

    @property
    def otpional(self):
        return self.optional
