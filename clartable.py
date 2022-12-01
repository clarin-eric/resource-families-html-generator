from pandas import DataFrame, Series
from typing import List, Set


class Tag:
    """
    Class for instancing tags in the tag tree outside <tbody>.

    :param tag_dict: JSON representation of tag rules (each line in rules.json specifies separate tag_dict,
                     tags can be nested)
    :type tag_dict: dict

    note:: tags enclosed by <tbody> in order to allow multiple rows generation without repeating headers are created using RowTag, not this class.
    """
    def __init__(self, tag_dict: dict):
        """
        Constructor for Tag instance
        """
        # Tag string, eg. <h1>
        self.tag: str
        # End tag string eg. </h1>
        self.end_tag: str
        # Tag content with variable placeholders (%s)
        self.text: str
        # Separator/connector tag if tag repeated, e.g. <br> in <p>foo</p><br><p>bar</p>
        self.on_next: str

        keys: Set[str] = set(tag_dict)

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
            # In order to allow repeatition of row generation, all tags within <tbody> ... </tbody>
            # are instances of RowTag, not Tag
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
    
    def generate(self, data_frame: DataFrame, stack: List) -> str:
        """
        Recursively generate tag tree

        :param data_frame: pandas DataFrame representing .csv content
        :type data_frame: pandas.DataFrame
        :param stack: List instance interpreted as tag stack for keeping track of unclosed tags
        :type: List

        :return: String representation of HTML tagtree
        :rtype: str
        """
        ret: str = ''
        intend = len(stack) * '\t'
        # <tbody> tag marks beginning of row tags 
        if self.tag == '<tbody>':
            # create table row for every data row in csv file
            for _, data_row in data_frame.iterrows():
                ret += intend + self.tag + self.text + '\n'
                stack.append(self.end_tag)
                for tag in self.tags:
                    ret += tag.generate(data_row, stack)
                end_tag = stack.pop()
                ret += intend + end_tag + '\n'
        else:
            ret = intend + self.tag + self.text + '\n'
            stack.append(self.end_tag)
            for tag in self.tags:
                ret += tag.generate(data_frame, stack)
            end_tag = stack.pop()
            ret += intend + end_tag + '\n'
        return ret


class RowTag:
    """
    Class for instancing tags in the tag tree within <tbody>

    :param tag_dict: JSON representation of tag rules, (each line in rules.json specifies separate tag_dict,
                     row tags can not be nested
    :type tag_dict: dict

    note:: RowTag is used for generation tags enclosed by <tbody> in order to allow multiple rows generation
           without repeating headers
    """

    def __init__(self, tag_dict):
        """
        Constructor for RowTag instance
        """
        # Tag string, eg. <h1>
        self.tag: str
        # End tag string eg. </h1>
        self.end_tag: str
        # Tag content with variable placeholders (%s)
        self.text: str
        # Separator/connector tag if tag repeated, e.g. <br> in <p>foo</p><br><p>bar</p>
        self.on_next: str

        keys: Set = set(tag_dict)
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

    def generate(self, data_row: Series, stack: list) -> str:
        """
        Recursively generate tag tree

        :param data_row: pandas Series representing .csv record data
        :type data_row: pandas.Series
        :param stack: List instance interpreted as tag stack for keeping track of unclosed tags
        :type stack: List

        :return: String representation of HTML tagtree
        :rtype: str
        """
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
    """
    Seed of a tag tree

    :param tag_dict: JSON representation of tag rules
    :type tag_dict: dict
    """
    def __init__(self, tag_dict):
        """
        Constructor for Clartable instance
        """
        super().__init__(tag_dict)
        # Stack for tracking opened tags
        self.tag_stack: list = []

    def generate(self, data_frame: DataFrame, stack: list = None) -> str:
        """
        Recursively generate tag tree

        :param data_frame: pandas DataFrame representing .csv record data
        :type data_row: pandas.DataFrame
        :param stack: List instance interpreted as tag stack for keeping track of unclosed tags
        :type stack: List

        :return: String representation of HTML tagtree
        :rtype: str
        """
        ret: str = ''
        stack = self.tag_stack
        for tag in self.tags:
            ret += tag.generate(data_frame, stack)
        return ret


class Field:
    """
    Fields are parts of the table which require data from .csv file, storing str with placeholders,
    e.g. "<strong>Size: </strong>%s"

    :param field_dict: dictionary with Field creation rules
    :type field_dict: dict
    """
    def __init__(self, field_dict: dict):
        """
        Constructor for Field instance
        """
        # Column names to fetch data from data row. Ordering of list members defines order of variable placeholders
        self.columns: List[str]
        # Ommit field if data field empty
        self.optional: bool
        # String with variable placeholders
        self.text: str
        # Separator placeholder, default '#SEP'
        self.sep: str

        self.optional = field_dict['optional']
        self.text = field_dict['text']
        self.columns = field_dict['columns']
        if 'sep' in field_dict.keys():
            self.sep = field_dict['sep']
        else:
            self.sep = None 

    def generate(self, data_row: Series) -> str:
        """
        Generate Field (a cell) in the table

        :param data_row: pandas Series representing .csv record data
        :type data_row: pandas.Series
        :param stack: List instance interpreted as tag stack for keeping track of unclosed tags
        :type stack: List

        :return: String representation of HTML table cell
        :rtype: str
        """
        ret: str = ''
        fields_data = [data_row[column] for column in self.columns]
        if self.optional:
            if all([field_data == '' for field_data in fields_data]):
                ret = ''
        if self.sep:
            split_lists = [[] for _ in range(len(self.columns))]
            for i, field_data in enumerate(fields_data):
                field_data_split = field_data.split(self.sep)
                if isinstance(field_data_split, list):
                    split_lists[i].extend(field_data_split)
                else:
                    split_lists[i].append(field_data_split)

            data = list(zip(*split_lists))
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

        elif len(fields_data) > 1:
            fields_data = tuple(fields_data)
            ret = self.text % fields_data
        else:
            fields_data = fields_data[0]
            ret = self.text % fields_data
        return ret
