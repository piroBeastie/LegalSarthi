import React from 'react';
import { CATEGORY_MAPPING } from '../../utils/constants';
import { Scale } from 'lucide-react';

const CategoryBadge = ({ category }) => {
  const cat = CATEGORY_MAPPING[category] || CATEGORY_MAPPING.general;
  const Icon = cat.icon || Scale;

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${cat.color}`}>
      <Icon className="mr-1 h-3 w-3" />
      {cat.label}
    </span>
  );
};

export default CategoryBadge;
