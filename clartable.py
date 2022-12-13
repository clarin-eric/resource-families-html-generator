from pandas import DataFrame, Series
from typing import List, Set


from utils import EmptyColumnError


class Tag:
    """
    Class for instancing tags in the tag tree outside <tbody>.
    :ivar tag: tag string, eg. <h1>
    :ivar end_tag: end tag string e.g. </h1>
    :ivar text: tag content with variable placeholders (%s)
    :ivar on_next: separator/connector tag if tag repeated, e.g. <br> in <p>foo</p><br><p>bar</p>


    note:: tags enclosed by <tbody> in order to allow multiple rows generation without repeating headers are created using RowTag, not this class.
    """
    def __init__(self, tag_dict: dict):
        """
        Constructor for Tag instance

        :param tag_dict: JSON representation of tag rules (each line in rules.json specifies separate tag_dict,
                     tags can be nested)
        :type tag_dict: dict
        """
        self.tag: str
        self.end_tag: str
        self.text: str
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

    :ivar tag: tag string, eg. <h1>
    :ivar end_tag: end tag string e.g. </h1>
    :ivar text: tag content with variable placeholders (%s)
    :ivar on_next: separator/connector tag if tag repeated, e.g. <br> in <p>foo</p><br><p>bar</p>

    note:: RowTag is used for generation tags enclosed by <tbody> in order to allow multiple rows generation
           without repeating headers
    """

    def __init__(self, tag_dict):
        """
        Constructor for RowTag instance

        :param tag_dict: JSON representation of tag rules, (each line in rules.json specifies separate tag_dict,
                         row tags can be nested
        :type tag_dict: dict
        """
        self.tag: str
        self.end_tag: str
        self.text: str
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

    :ivar tag_stack: stack keeping track of opened tags
    """
    def __init__(self, tag_dict):
        """
        Constructor for Clartable instance

        :param tag_dict: JSON representation of tag rules
        :type tag_dict: dict
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
    Fields are content of cells of HTML table which require data from .csv file, storing str with placeholders for data,
    e.g. "<strong>Size: </strong>%s"

    :ivar columns: list of column names containing data for the field
    :ivar ifempty: alternative rules for fields with empty data source
    :ivar optional: boolean, whether to ommit data field if data empty
    :ivar sep: separator placeholder, in default rules.json is set to '#SEP'
    :ivar text: string with variable placeholders

    """
    def __init__(self, field_dict: dict):
        """
        Constructor for Field instance

        :param field_dict: dictionary with Field creation rules
        :type field_dict: dict
        """
        self.columns: Set[str]
        self.optional: bool
        self.ifempty: dict
        self.sep: str
        self.text: str

        self.optional = field_dict['optional']
        self.text = field_dict['text']
        self.columns = field_dict['columns']
        if 'sep' in field_dict.keys():
            self.sep = field_dict['sep']
        else:
            self.sep = None

        if 'ifempty' in field_dict.keys():
            self.ifempty = field_dict["ifempty"]
        else:
            self.ifempty = {}

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
        ret: str
        text: str = self.text
        fields_data = [data_row[column] for column in self.columns]

        ret = ''
        # Check if data fields empty
        if not all([field_data == '' for field_data in fields_data]):
            empty_columns = {column for column in self.columns if data_row[column] == ''}
            # Check if rule exists
            if empty_columns and not self.optional and (not self.ifempty and all(set(ie["columns"]) for ie in self.ifempty) != empty_columns):
                raise EmptyColumnError(empty_columns)
            elif not self.optional:
                for ie in self.ifempty:
                    if set(ie["columns"]) == empty_columns:
                        text = ie["text"]
                        break
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
                ret += text % tmp
                ret += '\n'

        elif len(fields_data) > 1:
            fields_data = tuple(fields_data)
            ret = text % fields_data
        else:
            fields_data = fields_data[0]
            ret = text % fields_data
        return ret
