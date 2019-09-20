class Tag:
    '''
    Class for tags in the tag tree. Note, that tags enclosed by <tbody> in order to allow multiple rows generation without repeating headers are created using RowTag, not this class. 
    
    Args:
        tag_dict: JSON dict
    '''

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
            # in order to allow repeatition of row generation, all tags within <tbody> ... </tbody> are instances of RowTag, not Tag 
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
        '''
        Args:
            stack: [], a stack of strings in form of </tag> for tag enclosing
            data_frame: pandas.DataFrame to be passed in depth to the tree till it hits <tbody> tag

        Returns:
            string, generated html of a tag with its children
        '''
        intend = len(stack) * '\t'
        # <tbody> tag marks beginning of row tags 
        if self.tag == '<tbody>':
            ret = ''
            # create table row for every data row in csv file
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
    '''
    Class for tags in tag tree enclosed by <tbody>

    Args:
        tag_dict: JSON dict
    '''

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
    '''
    Seed of a tag tree
    
    Args:
        tag: JSON dict with table rules
    '''
    def __init__(self, tag):
        super().__init__(tag)
        self.tag_stack = []

    def generate(self, data_frame):
        ret = ''
        for tag in self.tags:
            ret += tag.generate(self.tag_stack, data_frame)
        return ret

class Field:
    '''
    Fields are parts of the table which require data from .csv file. Do not have a tag member, but stores its rules as a explicit text, e.g. "<strong>Size: </strong>%s"
    '''
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
        if len(fields_data) > 1:
            fields_data = tuple(fields_data)
        else:
            fields_data = fields_data[0]

        return self.text % fields_data

    @property
    def otpional(self):
        return self.optional
