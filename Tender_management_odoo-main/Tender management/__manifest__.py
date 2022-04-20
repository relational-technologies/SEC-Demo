
{
  "name"                 :  "Tender management",
  "summary"              :  "",
  "category"             :  "Website",

  "sequence"             :  1,
  "author"               :  "sonu",
  "license"              :  "Other proprietary",
  "website"              :  "",
  "description"          :  "",
  "live_test_url"        :  "",
  "depends"              :  [
                              'mail',

                            ],
  "data"                 :  [
                              'views/tenders_view.xml',
                              'views/enquiry.xml',
                                'views/estimation.xml',
                                'data/sequence.xml',
                                'views/settings.xml',
                                'security/ir.model.access.csv'
                            ],
  "images"               :  [],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  # "pre_init_hook"        :  "pre_init_check",
}
