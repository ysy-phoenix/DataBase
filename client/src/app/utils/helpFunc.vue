<script>
export function getTitle (title) {
  switch (title) {
    case 1:
      return '博士后';
    case 2:
      return '助教';
    case 3:
      return '讲师';
    case 4:
      return '副教授';
    case 5:
      return '特任教授';
    case 6:
      return '教授';
    case 7:
      return '助理研究员';
    case 8:
      return '特任副研究员';
    case 9:
      return '副研究员';
    case 10:
      return '特任研究员';
    case 11:
      return '研究员';
    default:
      return '';
  }
}

export function getGender (gender) {
  switch (gender) {
    case 1:
      return '男';
    case 2:
      return '女';
    default:
      return '';
  }
}

export function getPaperType (type) {
  switch (type) {
    case 1:
      return 'full paper';
    case 2:
      return 'short paper';
    case 3:
      return 'poster paper';
    case 4:
      return 'demo paper';
    default:
      return '';
  }
}

export function getPaperLevel (level) {
  switch (level) {
    case 1:
      return 'CCF-A';
    case 2:
      return 'CCF-B';
    case 3:
      return 'CCF-C';
    case 4:
      return '中文 CCF-A';
    case 5:
      return '中文 CCF-B';
    case 6:
      return '无级别';
    default:
      return '';
  }
}

export function getProjectType (type) {
  switch (type) {
    case 1:
      return '国家级项目';
    case 2:
      return '省部级项目';
    case 3:
      return '市厅级项目';
    case 4:
      return '企业合作项目';
    case 5:
      return '其它类型项目';
    default:
      return '';
  }
}

export function getSemester (semester) {
  switch (semester) {
    case 1:
      return '春季学期';
    case 2:
      return '夏季学期';
    case 3:
      return '秋季学期';
    default:
      return '';
  }
}

export function getCourseType (type) {
  switch (type) {
    case 1:
      return '本科生课程';
    case 2:
      return '研究生课程';
    default:
      return '';
  }
}
</script>