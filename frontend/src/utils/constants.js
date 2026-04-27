import { Shield, ShoppingBag, Home, Briefcase, Monitor, Heart, FileText, TreePine, Scale } from 'lucide-react';

export const CATEGORY_MAPPING = {
  police: { icon: Shield, color: 'bg-primary border border-blue-900/50 text-blue-400', label: 'Police', emoji: '🚔' },
  consumer: { icon: ShoppingBag, color: 'bg-primary border border-orange-900/50 text-orange-400', label: 'Consumer', emoji: '🛒' },
  property: { icon: Home, color: 'bg-primary border border-green-900/50 text-green-400', label: 'Property', emoji: '🏠' },
  workplace: { icon: Briefcase, color: 'bg-primary border border-purple-900/50 text-purple-400', label: 'Workplace', emoji: '💼' },
  cyber: { icon: Monitor, color: 'bg-primary border border-indigo-900/50 text-indigo-400', label: 'Cyber', emoji: '💻' },
  domestic: { icon: Heart, color: 'bg-primary border border-red-900/50 text-red-400', label: 'Domestic', emoji: '🏠' },
  rti: { icon: FileText, color: 'bg-primary border border-teal-900/50 text-teal-400', label: 'RTI', emoji: '📄' },
  environment: { icon: TreePine, color: 'bg-primary border border-emerald-900/50 text-emerald-400', label: 'Environment', emoji: '🌿' },
  general: { icon: Scale, color: 'bg-primary border border-border-color text-text-muted', label: 'General', emoji: '⚖️' },
};
