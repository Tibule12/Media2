import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PostDetail from '../PostDetail.vue';

describe('PostDetail.vue', () => {
  it('renders post detail container', () => {
    const wrapper = mount(PostDetail);
    expect(wrapper.exists()).toBe(true);
  });
});
