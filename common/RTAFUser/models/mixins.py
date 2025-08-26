class RTAFUserMixins():
    def get_full_name(self):
        if self.rank_id:
            return "{}{} {}".format(self.rank.short_display, self.first_name, self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
    get_full_name.short_description = 'ยศ ชื่อ-สกุล'
