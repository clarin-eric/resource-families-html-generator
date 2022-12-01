from typing import List


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
    
    def generate(self, data_frame, stack):
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
                    ret += tag.generate(data_row, stack)
                end_tag = stack.pop()
                ret += intend + end_tag + '\n'
            return ret
        else:
            ret = intend + self.tag + self.text + '\n'
            stack.append(self.end_tag)
            for tag in self.tags:
                ret += tag.generate(data_frame, stack)
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

    def generate(self, data_row, stack: list) -> str:
        intend = len(stack) * '\t'
        ret = intend + self.tag + self.text + '\n'
        stack.append(self.end_tag)

        for tag in self.tags:
            ret += tag.generate(data_row, stack)

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
        self.tag_stack: list = []

    def generate(self, data_frame, stack: list = None) -> str:
        ret = ''
        stack = self.tag_stack
        for tag in self.tags:
            ret += tag.generate(data_frame, stack)
        return ret


class Field:
    '''
    Fields are parts of the table which require data from .csv file, but stores text, e.g. "<strong>Size: </strong>%s"
    '''
    def __init__(self, field_dict):
        self.optional: bool = field_dict['optional']
        self.text: str = field_dict['text']
        self.columns: List[str] = field_dict['columns']
        if 'sep' in field_dict.keys():
            self.sep = field_dict['sep']
        else:
            self.sep = None 

    def generate(self, data_row):
        fields_data = [data_row[column] for column in self.columns]
        if self.optional:
            if all([field_data == '' for field_data in fields_data]):
                return ''
        if self.sep:
            split_lists = [[] for i in range(len(self.columns))]
            for i, field_data in enumerate(fields_data):
                field_data_split = field_data.split(self.sep)
                if isinstance(field_data_split, list):
                    split_lists[i].extend(field_data_split)
                else:
                    split_lists[i].append(field_data_split)

            data = list(zip(*split_lists))
            ret = ''
            for fields_data in data:
                tmp = fields_data
                #TODO find a way to remove hardcoded button icons
                if 'Buttons' in self.columns:
                    if 'Download' in fields_data:
                        tmp = fields_data[:1] + ('fa fa-arrow-circle-o-down',) + fields_data[1:]
                    else:
                        tmp = fields_data[:1] + ('fa fa-search',) + fields_data[1:]
                ret += self.text % tmp 
                ret += '\n'
            return ret

        elif len(fields_data) > 1:
            fields_data = tuple(fields_data)
        else:
            fields_data = fields_data[0]

        return self.text % fields_data

    @property
    def otpional(self):
        return self.optional
